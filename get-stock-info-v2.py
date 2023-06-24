
#https://finance.yahoo.com/quote/INFY.BO/history?period1=1653372093&period2=1684908093&interval=capitalGain%7Cdiv%7Csplit&filter=capitalGain&frequency=1d&includeAdjustedClose=true
#https://pypi.org/project/yahooquery/

from yahooquery import Ticker
import pandas as pd
from utils import get_dates_v2, get_dates, write_to_csv, write_to_xls
import datetime

# lot of changes are done afte 23rd Jun which are not in get_stock_info.py

def process(stock, startDate, endDate, ):
    df = stock.history(start=startDate, end=endDate)
    # print(df)
    stock_close = df['close']
    # print(stock,stock_close[0])
    return stock_close

# input, read csv

def get_stock_data(datesDataFrame):
    
    filedf = pd.read_csv('input.csv')
    csv_obj = [["Share", "5y", "2y", "1y", "6m", "3m", "1m", "5D", "Today"]]

    # print(df)

    for idx, s in enumerate(filedf.get('Shares')):
        stock_values = [s]
        # print(s)
        # stock = Ticker(s+".BO").history(start=datesDataFrame['start_date'][6], end=datesDataFrame['end_date'][6], )
        # print(stock)

        stock = Ticker(s+".BO")

        id = 0

        # 5y
        if(idx==0):
            print(csv_obj[0][id+1] + ': ' + datesDataFrame['start_date'][id])

        stock_close = process(stock, datesDataFrame['start_date'][id], datesDataFrame['end_date'][id])
        stock_values.append(int(stock_close.get(0, 0)))

        # 2y
        id = id + 1
        if(idx==0):
            print(csv_obj[0][id+1] + ': ' + datesDataFrame['start_date'][id])
        stock_close = process(stock, datesDataFrame['start_date'][id], datesDataFrame['end_date'][id])
        stock_values.append(int(stock_close.get(0, 0)))

        # 1y
        id = id + 1
        if(idx==0):
            print(csv_obj[0][id+1] + ': ' + datesDataFrame['start_date'][id])
        stock_close = process(stock, datesDataFrame['start_date'][id], datesDataFrame['end_date'][id])
        stock_values.append(int(stock_close.get(0, 0)))

        # 6m
        id = id + 1
        if(idx==0):
            print(csv_obj[0][id+1] + ': ' + datesDataFrame['start_date'][id])
        stock_close = process(stock, datesDataFrame['start_date'][id], datesDataFrame['end_date'][id])
        stock_values.append(int(stock_close.get(0, 0)))

        # 3m
        id = id + 1
        if(idx==0):
            print(csv_obj[0][id+1] + ': ' + datesDataFrame['start_date'][id])
        stock_close = process(stock, datesDataFrame['start_date'][id], datesDataFrame['end_date'][id])
        stock_values.append(int(stock_close.get(0, 0)))

        # 1m
        id = id + 1
        if(idx==0):
            print(csv_obj[0][id+1] + ': ' + datesDataFrame['start_date'][id])
        stock_close = process(stock, datesDataFrame['start_date'][id], datesDataFrame['end_date'][id])
        stock_values.append(int(stock_close.get(0, 0)))


        # 5d
        id = id + 1
        if(idx==0):
            print(csv_obj[0][id+1] + ': ' + datesDataFrame['start_date'][id])
        stock_close = process(stock, datesDataFrame['start_date'][id], datesDataFrame['end_date'][id])
        stock_values.append(int(stock_close.get(0, 0)))

        # today
        id = id + 1
        if(idx==0):
            print(csv_obj[0][id+1] + ': ' + datesDataFrame['start_date'][id])
        stock_close = process(stock, datesDataFrame['start_date'][id], datesDataFrame['end_date'][id])
        stock_values.append(int(stock_close.get(0, 0)))

        csv_obj.append(stock_values)
        
    print(csv_obj)

    return csv_obj

def main():

    # 1. get the dates for which data is required
    datesDataFrame = get_dates_v2()

    # 2. get the final data obj
    csv_obj = get_stock_data(datesDataFrame)

    # 3. write to file
    # write_to_csv(csv_obj, datetime.date.today().strftime('%Y-%b-%d')+"-v2.tsv")
    write_to_xls(csv_obj, datetime.date.today().strftime('%Y-%b-%d')+"-v2")


if __name__ == '__main__':
    main()