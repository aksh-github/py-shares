
#https://finance.yahoo.com/quote/INFY.BO/history?period1=1653372093&period2=1684908093&interval=capitalGain%7Cdiv%7Csplit&filter=capitalGain&frequency=1d&includeAdjustedClose=true
#https://pypi.org/project/yfinance/

import yfinance as yf
import pandas as pd
import csv
from utils import get_dates, write_to_csv
import datetime

def process(stock, startDate, endDate, ):
    df = stock.history(start=startDate, end=endDate, actions=False, rounding=True)
    # print(df)
    stock_close = df['Close']
    # print(stock,stock_close[0])
    return stock_close

# input, read csv

def get_stock_data(datesDataFrame):
    
    filedf = pd.read_csv('input.csv')
    csv_obj = [["Share", "Today", "5y", "1y", "6m", "3m", "1m", "5D"]]

    # print(df)

    for idx, s in enumerate(filedf.get('Shares')):
        stock_values = [s]
        # print(s)
        stock = yf.Ticker(s+".BO")

        # today
        #df = stock.history(start=datesDataFrame['start_date'][5], end=datesDataFrame['end_date'][5], actions=False, rounding=True)
        stock_close = process(stock, datesDataFrame['start_date'][6], datesDataFrame['end_date'][6])
        # stock_values.append(stock_close[0])
        stock_values.append(stock_close.get(0, 0))

        # 5y
        stock_close = process(stock, datesDataFrame['start_date'][0], datesDataFrame['end_date'][0])
        # stock_values.append(stock_close[0])
        stock_values.append(stock_close.get(0, 0))

        # 1y
        stock_close = process(stock, datesDataFrame['start_date'][1], datesDataFrame['end_date'][1])
        # stock_values.append(stock_close[0])
        stock_values.append(stock_close.get(0, 0))

        # 6m
        stock_close = process(stock, datesDataFrame['start_date'][2], datesDataFrame['end_date'][2])
        # stock_values.append(stock_close[0])
        stock_values.append(stock_close.get(0, 0))

        # 3m
        stock_close = process(stock, datesDataFrame['start_date'][3], datesDataFrame['end_date'][3])
        # stock_values.append(stock_close[0])
        stock_values.append(stock_close.get(0, 0))

        # 1m
        stock_close = process(stock, datesDataFrame['start_date'][4], datesDataFrame['end_date'][4])
        # stock_values.append(stock_close[0])
        stock_values.append(stock_close.get(0, 0))

        # 5d
        stock_close = process(stock, datesDataFrame['start_date'][5], datesDataFrame['end_date'][5])
        # stock_values.append(stock_close[0])
        stock_values.append(stock_close.get(0, 0))

        csv_obj.append(stock_values)
        # stock_values = []
        
        # print(s, stock_values)
        # print('====================')

    print(csv_obj)
    return csv_obj

def main():

    # 1. get the dates for which data is required
    datesDataFrame = get_dates()

    # 2. get the final data obj
    csv_obj = get_stock_data(datesDataFrame)

    # 3. write to csv
    write_to_csv(csv_obj, datetime.date.today().strftime('%Y-%b-%d')+".tsv")

if __name__ == '__main__':
    main()