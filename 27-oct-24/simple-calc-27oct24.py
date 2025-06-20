import datetime
import uuid
import yfinance as yf
import pandas as pd
import os
# os.chdir('./27-oct-24')

# import requests 
# new package added to overcome rate limit error
# https://github.com/ranaroussi/yfinance/issues/2422#issuecomment-2840774505 (see answer from TianqiMikeHu or alindsaydiaz)

from curl_cffi import requests

extra_path = './27-oct-24'
# extra_path = './'

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


data_cache = {}

def get_top_stock_data(stock_file_path, output_eom_path_xl, option):

    # Define the file path for the text file containing stock names
    # stock_file_path = './27-oct-24/stock_names.txt'

    # Define the file path for the output CSV file
    # output_summary_path_xl = "{}/stock_summary-{}.xlsx".format(extra_path, str(uuid.uuid4().hex[:8])) # f"{extra_path}/stock_summary-{uuid.uuid4()[:8])
    output_eom_path_xl = "{}/{}".format(extra_path, output_eom_path_xl) # f"{extra_path}/monthly-highs-{uuid.uuid4()[:8]}.xlsx"

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

        # break out of loop if stock name is empty or starts with '#'
                
        if not stock_name or stock_name.startswith('#'):
            break

        try:
            print('Getting data for: ' + stock_name)
            session = requests.Session(impersonate="chrome")
            # data = yf.download(stock_name, period='1y')

            if data_cache.get(stock_name) is not None:
                data = data_cache[stock_name]
                print(f"******** Using cached data for {stock_name}")
            else:
                data = yf.Ticker(stock_name, session=session).history(period='3mo')

            if data is None or data.empty:
                print(f"Error fetching data for {stock_name}: empty or null data")
                continue

            data_cache[stock_name] = data

            # 1. % change (speed calculation) between last year price and current price and show top 5 

            stock_data = speed(stock_data, stock_name, data)

            # end % change (speed calculation)


            # 2. Get monthly max / avg etc price for last 12 months and write to excel

            if option == 'max':
                eomStockData = data.resample('M').max()     # Get monthly max close price
                sheet_name = 'Max'
            elif option == 'avg':
                eomStockData = data.resample('M').mean()    # Get monthly average close price
                sheet_name = 'Avg'
            else:
                print('Invalid option for Resampling. Please choose either "max" or "avg"')
                exit()
            # eomStockData = data.resample('M').mean()    # Get monthly average close price (works correctly 19-jun-2025)
            # eomStockData = data.resample('M').max()     # Get monthly max close price  (works correctly 19-jun-2025)
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

    
    # only for existing stocks
    bottom5 = sorted_data.tail(5).reset_index(drop=True)

    # Send the data as a message to Telegram
    try:
        send_telegram_message(top5[["Stock", "Curr Price", "LYr-Curr % Chg"]].to_string(index=False))
        send_telegram_message(bottom5[["Stock", "Curr Price", "LYr-Curr % Chg"]].to_string(index=False))
        
    except Exception as e:
        print(f"Data was not sent to Telegram: {str(e)}")

    # monthly data
    # print(dfs)

    # Concatenate the list of DataFrames
    if not dfs:
        print("No data found for any of the stocks")
        exit()

    df = pd.concat(dfs, axis=1)

    # Convert the date index to 'MMM-YY' format
    df.index = df.index.strftime('%b-%y')

    # Transpose the DataFrame
    df = df.T

    # Write the DataFrame to an Excel file
    
    if os.path.isfile(output_eom_path_xl):
        # Append to existing file
        with pd.ExcelWriter(output_eom_path_xl, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=sheet_name, header=True, index=True)
    else:
        # Create new file
        df.to_excel(output_eom_path_xl, sheet_name=sheet_name, header=True, index=True)

def speed(stock_data, stock_name, data):
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
    return stock_data

    # end monthly data


    # Save the data to an Excel file
    # try:
    #     stock_data.to_excel(output_summary_path_xl, index=False)
    # except Exception as e:
    #     print(f"Error saving data to {output_summary_path_xl}: {str(e)}")
    #     exit()

    # print("Data saved to", output_summary_path_xl)

def main(stock_file_path):
    output_eom_path_xl = f'eom-data-{datetime.date.today().strftime("%d-%b")}-{str(uuid.uuid4())[:8]}.xlsx'
    # print(output_eom_path_xl)
    get_top_stock_data(stock_file_path, output_eom_path_xl=output_eom_path_xl, option = "max")
    get_top_stock_data(stock_file_path, output_eom_path_xl=output_eom_path_xl, option = "avg")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        stock_file_path = sys.argv[1]
    else:
        # Use the default file path
        stock_file_path = f'{extra_path}/stocks.txt'
    main(stock_file_path)

