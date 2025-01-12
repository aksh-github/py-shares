import yfinance as yf
import matplotlib.pyplot as plt

extra_path = './27-oct-24'

def get_top_stock_data(stock_file_path):

    # Create a figure and axis
    fig, ax = plt.subplots()

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

    # Fetch the data for each stock and extract the required prices
    for stock_name in stock_names:

        # break out of loop if stock name is empty or starts with '#'
        if not stock_name or stock_name.startswith('#'):
            break

        try:
            print('Getting data for: ' + stock_name)
            # data = yf.download(stock_name, period='1y')
            data = yf.Ticker(stock_name).history(period='1mo')
            if data is None or data.empty:
                print(f"Error fetching data for {stock_name}: empty or null data")
                continue

            # Calculate the relative percentage change
            data['Relative Change'] = (data['Close'] / data['Close'].iloc[0] - 1) * 100
            
            # Resample the data to monthly frequency
            # monthly_data = data['Relative Change'].resample('M').last()
            # Get monthly average close price
            monthly_data = data['Relative Change'].resample('M').mean() 
            
            # Plot the relative percentage change
            ax.plot(monthly_data, label=stock_name, marker='o')

        except Exception as e:
            print(f"Error fetching data for {stock_name}: {str(e)}")

    # Set the title and labels
    ax.set_title('Relative Percentage Change of Stocks')
    ax.set_xlabel('Months')
    ax.set_ylabel('Relative Percentage Change (%)')

    # Add a legend
    ax.legend()

    # Show the plot
    plt.show()

    # Save the plot to a file
    # plt.savefig('./relative_percentage_change.png')

    # Close the plot
    plt.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        stock_file_path = sys.argv[1]
    else:
        # Use the default file path
        stock_file_path = f'{extra_path}/stocks.txt'
    get_top_stock_data(stock_file_path)