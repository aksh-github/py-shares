import uuid
import yfinance as yf
import pandas as pd

# Define the file path for the text file containing stock names
stock_file_path = './27-oct-24/stock_names.txt'

# Define the file path for the output CSV file
output_file_path = './27-oct-24/stock_data.csv'
output_summary_path = './27-oct-24/stock_summary.csv'
output_summary_path_xl = "./27-oct-24/stock_summary" + '-' + str(uuid.uuid4())[:8] + ".xlsx"

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

# Fetch the data for each stock and extract the required prices
for stock_name in stock_names:
    try:
        print('Getting data for: ' + stock_name)
        # data = yf.download(stock_name, period='1y')
        data = yf.Ticker(stock_name).history(period='1y')
        if data is None or data.empty:
            print(f"Error fetching data for {stock_name}: empty or null data")
            continue
        last_year_price = round(data['Close'].iloc[0] if data['Close'].iloc[0] is not None else 0, 2)
        top_price = round(data['Close'].max() if data['Close'].max() is not None else 0)
        current_price = round(data['Close'].iloc[-1] if data['Close'].iloc[-1] is not None else 0)


        LY_percent_change = round(((top_price - last_year_price) / last_year_price) * 100, 2)
        current_percent_change = round(((top_price - current_price) / current_price) * 100, 2)
        
        # calculate the % change between last year price and current price
        last_Curr_percent_change = round(((current_price - last_year_price) / last_year_price) * 100, 2)


        if top_price > current_price:
            current_percent_change = -current_percent_change
        
        stock_data = pd.concat([stock_data, pd.DataFrame({'Stock': [stock_name], 'LYr Price': [last_year_price], 'Top Price': [top_price], 'Curr Price': [current_price], 'LYr % Chg': [LY_percent_change], 'Curr % Chg': [current_percent_change] , 'LYr-Curr % Chg': [last_Curr_percent_change]})], ignore_index=True)
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
print(sorted_data.head(5))

# Save the data to a CSV file
# stock_data.to_csv(output_summary_path, index=False)

# try:
#     stock_data.to_excel(output_summary_path_xl, index=False)
# except Exception as e:
#     print(f"Error saving data to {output_summary_path_xl}: {str(e)}")
#     exit()

print("Data saved to", output_summary_path_xl)