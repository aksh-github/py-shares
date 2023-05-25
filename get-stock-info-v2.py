
#https://finance.yahoo.com/quote/INFY.BO/history?period1=1653372093&period2=1684908093&interval=capitalGain%7Cdiv%7Csplit&filter=capitalGain&frequency=1d&includeAdjustedClose=true
#https://pypi.org/project/yfinance/

from yahooquery import Ticker
import pandas as pd
import csv
from getdates import get_dates
import datetime

def write_to_csv(data):
    
    with open(datetime.date.today().strftime('%Y-%b-%d')+"-v2.csv", "w", newline='') as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(data)

def process(stock, startDate, endDate, ):
    df = stock.history(start=startDate, end=endDate)
    # print(df)
    stock_close = df['close']
    # print(stock,stock_close[0])
    return stock_close

# input, read csv

def get_stock_data(datesDataFrame):
    
    filedf = pd.read_csv('input.csv')
    csv_obj = [["Share", "Today", "5D"]]

    # print(df)

    for idx, s in enumerate(filedf.get('Shares')):
        stock_values = [s]
        # print(s)
        # stock = Ticker(s+".BO").history(start=datesDataFrame['start_date'][6], end=datesDataFrame['end_date'][6], )
        # print(stock)

        stock = Ticker(s+".BO")
    
        stock_close = process(stock, datesDataFrame['start_date'][6], datesDataFrame['end_date'][6])
        stock_values.append(stock_close[0])

        stock_close = process(stock, datesDataFrame['start_date'][5], datesDataFrame['end_date'][5])
        stock_values.append(stock_close[0])

        csv_obj.append(stock_values)
        
    print(csv_obj)

# write to csv
    write_to_csv(csv_obj)


# print(get_dates())

datesDataFrame = get_dates()

# print(datesDataFrame['start_date'][0])

get_stock_data(datesDataFrame)



# correct
# shares = ["TCS", "WIPRO"]
# for s in shares:
#     stock = yf.Ticker(s+".BO")
#     df = stock.history(period="1d")
#     print(s+".BO", df['Close'][0])


# stock = yf.Ticker("HCLTECH.BO")
# d1 = stock.history(period="1d")
# print(d1)   # works

# df = pd.DataFrame(d1)

# print(d1['Close'], df.get('Close'))   # works

# print(d1)

# print(d1['Close'][0], d1.get('Close')[0])   # gives final val perfect

# print(df.to_json("./tp.json"))  # works


