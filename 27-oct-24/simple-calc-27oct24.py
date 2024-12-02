import uuid
import yfinance as yf
import pandas as pd
import os
# os.chdir('./27-oct-24')

import requests

def send_telegram_message(message):

    # print(os.getcwd())
    # most easy way is define env variables in proj root folder in .env file

    TOKEN = os.getenv('TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')

    # print(TOKEN, CHAT_ID)

    try:
        if not TOKEN or not CHAT_ID:
            raise ValueError("TOKEN or CHAT_ID not found in config file")
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        data = {'chat_id': CHAT_ID, 'text': message}

        # print(url, data)
        
        # Send the request
        response = requests.post(url, json=data)

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print("Error sending message:")
            print(response.text)
    except ValueError as e:
        print(e)
        # exit()

def get_top_stock_data(stock_file_path):

    # Define the file path for the text file containing stock names
    # stock_file_path = './27-oct-24/stock_names.txt'

    # Define the file path for the output CSV file
    output_summary_path_xl = "./27-oct-24/stock_summary" + '-' + str(uuid.uuid4())[:8] + ".xlsx"
    output_eom_path_xl = "./27-oct-24/eom_closes" + '-' + str(uuid.uuid4())[:8] + ".xlsx"

    # Read the stock names from the text file
    try:
        with open(stock_file_path, 'r') as file:
            stock_names = [line.strip() for line in file.readlines() if line]
            if not stock_names:
                print(f"File {stock_file_path} is empty.")
                exit()
    except FileNotFoundError:
        print(f"File {stock_file_path} not found.")
        exit()
    except Exception as e:
        print(f"Error reading file {stock_file_path}: {str(e)}")
        exit()

    # Create an empty DataFrame to store the stock data
    stock_data = pd.DataFrame(columns=['Stock', 'LYr Price', 'Top Price', 'Curr Price', 'LYr % Chg', 'Curr % Chg', 'LYr-Curr % Chg'])

    # eomAllStockData = pd.DataFrame(columns=['Stock', 'Date1', 'Date2', 'Date3', 'Date4', 'Date5', 'Date6', 'Date7', 'Date8', 'Date9', 'Date10', 'Date11', 'Date12'])
    dfs = []

    # Fetch the data for each stock and extract the required prices
    for stock_name in stock_names:
        try:
            print('Getting data for: ' + stock_name)
            # data = yf.download(stock_name, period='1y')
            data = yf.Ticker(stock_name).history(period='1y')
            if data is None or data.empty:
                print(f"Error fetching data for {stock_name}: empty or null data")
                continue

            # 1. % change (speed calculation)

            last_year_price = round(data['Close'].iloc[0] if data['Close'].iloc[0] is not None else 0, 2)
            top_price = round(data['Close'].max() if data['Close'].max() is not None else 0)
            current_price = round(data['Close'].iloc[-1] if data['Close'].iloc[-1] is not None else 0)


            LY_percent_change = round(((top_price - last_year_price) / last_year_price) * 100, 2)
            current_percent_change = round(((top_price - current_price) / current_price) * 100, 2)
            
            # calculate the % change between last year price and current price
            last_Curr_percent_change = round(((current_price - last_year_price) / last_year_price) * 100, 2)


            if top_price > current_price:
                current_percent_change = -current_percent_change
            
            stock_data = pd.concat([stock_data, pd.DataFrame({'Stock': [stock_name.replace('.NS', '').replace('.BO', '')], 'LYr Price': [last_year_price], 'Top Price': [top_price], 'Curr Price': [current_price], 'LYr % Chg': [LY_percent_change], 'Curr % Chg': [current_percent_change] , 'LYr-Curr % Chg': [last_Curr_percent_change]})], ignore_index=True)

            # end % change (speed calculation)


            # 2. Get monthly close price

            eomStockData = data.resample('ME').max()
            # print(eomStockData)
            
            # Select only the 'Close' column
            closing_prices = eomStockData.loc[:, ['Close']].round(2)
            
            # Rename the column to include the stock symbol
            closing_prices = closing_prices.rename(columns={'Close': stock_name.replace('.NS', '').replace('.BO', '')})
            
            # Merge the closing prices with the existing DataFrame
            

            # eomAllStockData = pd.concat([eomAllStockData, closing_prices], axis=1)
            # print(closing_prices)

            dfs.append(closing_prices)

            # end Get monthly close price

        except Exception as e:
            print(f"Error fetching data for {stock_name}: {str(e)}")

    # Print the stock data
    # print(stock_data)

    # Sort the stock data by LYr % Change
    # sorted_data = stock_data.sort_values(by='LYr % Chg', ascending=False)
    # print(sorted_data.head(5))

    # Sort the stock data by Curr % Change
    # sorted_data = stock_data.sort_values(by='Curr % Chg', ascending=False)
    # print(sorted_data.head(5))

    # Sort the stock data by LYr-Curr % Change
    sorted_data = stock_data.sort_values(by='LYr-Curr % Chg', ascending=False)
    # print(sorted_data.head(5))
    top5 = sorted_data.head(5).reset_index(drop=True)
    print(top5.to_string(index=False))

    # Send the data as a message to Telegram
    try:
        send_telegram_message(top5[["Stock", "Curr Price", "LYr-Curr % Chg"]].to_string(index=False))
    except Exception as e:
        print(f"Data was not sent to Telegram: {str(e)}")

    # monthly data
    # print(dfs)

    # Concatenate the list of DataFrames
    df = pd.concat(dfs, axis=1)

    # Convert the date index to 'MMM-YY' format
    df.index = df.index.strftime('%b-%y')

    # Transpose the DataFrame
    df = df.T

    # Write the DataFrame to an Excel file
    df.to_excel(output_eom_path_xl, header=True, index=True)

    # end monthly data


    # Save the data to an Excel file
    # try:
    #     stock_data.to_excel(output_summary_path_xl, index=False)
    # except Exception as e:
    #     print(f"Error saving data to {output_summary_path_xl}: {str(e)}")
    #     exit()

    # print("Data saved to", output_summary_path_xl)

def main(stock_file_path):
    get_top_stock_data(stock_file_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        stock_file_path = sys.argv[1]
    else:
        # Use the default file path
        stock_file_path = './27-oct-24/stock_names.txt'
    main(stock_file_path)

