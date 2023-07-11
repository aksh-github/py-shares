
#https://finance.yahoo.com/quote/INFY.BO/history?period1=1653372093&period2=1684908093&interval=capitalGain%7Cdiv%7Csplit&filter=capitalGain&frequency=1d&includeAdjustedClose=true
#https://pypi.org/project/yahooquery/

from yahooquery import Ticker
import pandas as pd
from utils import get_dates_v2, write_to_xls
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
    csv_obj = [["Share", "5y", "2y", "1y", "6m", "3m", "1m", "5d", "Today"]]

    # print(df)

    for idx, s in enumerate(filedf.get('Shares')):
        stock_values = [s]
        
        stock = Ticker(s+".NS")

        id = 0

        for tp in csv_obj[0][1:]:
            if(idx==0):
                print(tp + ': ' + datesDataFrame['start_date'][id])

            stock_close = process(stock, datesDataFrame['start_date'][id], datesDataFrame['end_date'][id])
            stock_values.append(int(stock_close.get(0, 0)))

            id = id + 1

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