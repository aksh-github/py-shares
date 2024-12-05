import yfinance as yf
import matplotlib.pyplot as plt

# Define the stock symbols
stock_symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

# Define the time period
period = '1y'

# Create a figure and axis
fig, ax = plt.subplots()

# Loop through each stock symbol
for symbol in stock_symbols:
    # Download the stock data
    data = yf.download(symbol, period=period)
    
    # Calculate the relative percentage change
    data['Relative Change'] = (data['Close'] / data['Close'].iloc[0] - 1) * 100
    
    # Resample the data to monthly frequency
    monthly_data = data['Relative Change'].resample('ME').last()
    
    # Plot the relative percentage change
    ax.plot(monthly_data, label=symbol, marker='o')

# Set the title and labels
ax.set_title('Relative Percentage Change of Stocks')
ax.set_xlabel('Months')
ax.set_ylabel('Relative Percentage Change (%)')

# Add a legend
ax.legend()

# Show the plot
# plt.show()

# Save the plot to a file
plt.savefig('./relative_percentage_change.png')