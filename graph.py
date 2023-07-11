import matplotlib.pyplot as plt

# # Stock data for multiple stocks
# stocks = {
#     'AAPL': [150, 160, 170, 165, 155],
#     'GOOGL': [2000, 2100, 2200, 2150, 2050],
#     'MSFT': [300, 310, 320, 325, 315]
# }


import csv

# Open the CSV file
with open('async.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    
    # Read the header row if present
    header = next(csv_reader)
    
    # Create an empty dictionary
    data = {}
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the key and values from the row
        key = row[0]
        values = row[1:]

        # print(type (values))

        arr = []

        for item in values:
            arr.append(int(item))
        # Assign the values to the dictionary
        # data[key] = values
        data[key] = arr

# Print the dictionary
print(data)

# Plotting the data for each stock
for stock, values in data.items():
    plt.plot(values, label=stock)

# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Stock Value')
plt.title('Stock Performance')

# Adding legend
plt.legend()

# Display the plot
plt.show()