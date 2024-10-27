import yfinance as yf
import pandas as pd

# Define the file path for the text file containing stock names
stock_file_path = './27-oct-24/stock_names.txt'

# Define the file path for the output CSV file
output_file_path = './27-oct-24/stock_data.csv'
output_summary_path = './27-oct-24/stock_summary.csv'

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
stock_data = pd.DataFrame(columns=['Stock', 'Last Year Price', 'Top Price', 'Latest Price'])

# Fetch the data for each stock and extract the required prices
for stock_name in stock_names:
    try:
        print('Getting data for: ' + stock_name)
        data = yf.download(stock_name, period='1y')
        first_day_price = round(data['Close'].iloc[0], 2)
        top_price = round(data['Close'].max())
        latest_price = round(data['Close'].iloc[-1])
        stock_data = pd.concat([stock_data, pd.DataFrame({'Stock': [stock_name], 'First Day Price': [first_day_price], 'Top Price': [top_price], 'Latest Price': [latest_price]})])
    except Exception as e:
        print(f"Error fetching data for {stock_name}: {str(e)}")

# Print the stock data
print(stock_data)

# Save the data to a CSV file
stock_data.to_csv(output_summary_path, index=False)

print("Data saved to", output_summary_path)