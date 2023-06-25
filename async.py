
from yahooquery import Ticker
from datetime import datetime
import pandas as pd
from utils import get_dates_v2, get_dates, write_to_xls
import datetime

symbols = ['fb', 'aapl', 'amzn', 'nflx', 'goog']

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("b4 =", current_time)

# faang = Ticker(symbols).history(period="1d")

# print(faang)

# now = datetime.now()

# current_time = now.strftime("%H:%M:%S")
# print("after =", current_time)

def process(stock, startDate, endDate, ):
    df = stock.history(start=startDate, end=endDate)
    # print(df)
    stock_close = df['close']
    # print(stock,stock_close[0])
    return stock_close

# input, read csv

def get_stock_data(datesDataFrame):
    
    filedf = pd.read_csv('input.csv')
    csv_obj = [["Share", "5y", "1y", "6m", "3m", "1m", "5D", "Today"]]

    # print(df)

    # for idx, s in enumerate(filedf.get('Shares')):
    stock_values = ["RVNL.BO, tcs.BO, INFY.BO, sbi.BO"]
    # print(s)
    # stock = Ticker(s+".BO").history(start=datesDataFrame['start_date'][6], end=datesDataFrame['end_date'][6], )
    # print(stock)

    # stock = Ticker(s+".BO")
    stock = Ticker("RVNL.BO tcs.BO INFY.BO sbi.BO", asynchronous=True)

    # 5y
    stock_close = process(stock, datesDataFrame['start_date'][0], datesDataFrame['end_date'][0])
    # stock_values.append(int(stock_close[0]))
    stock_values.append(int(stock_close.get(0, 0)))

    # 1y
    stock_close = process(stock, datesDataFrame['start_date'][1], datesDataFrame['end_date'][1])
    # stock_values.append(int(stock_close[0]))
    stock_values.append(int(stock_close.get(0, 0)))

    # 6m
    stock_close = process(stock, datesDataFrame['start_date'][2], datesDataFrame['end_date'][2])
    # stock_values.append(int(stock_close[0]))
    stock_values.append(int(stock_close.get(0, 0)))

    # 3m
    stock_close = process(stock, datesDataFrame['start_date'][3], datesDataFrame['end_date'][3])
    # stock_values.append(int(stock_close[0]))
    stock_values.append(int(stock_close.get(0, 0)))

    # 1m
    stock_close = process(stock, datesDataFrame['start_date'][4], datesDataFrame['end_date'][4])
    # stock_values.append(int(stock_close[0]))
    stock_values.append(int(stock_close.get(0, 0)))


    # 5d
    stock_close = process(stock, datesDataFrame['start_date'][5], datesDataFrame['end_date'][5])
    # stock_values.append(int(stock_close[0]))
    stock_values.append(int(stock_close.get(0, 0)))

    # today
    stock_close = process(stock, datesDataFrame['start_date'][6], datesDataFrame['end_date'][6])
    # stock_values.append(int(stock_close[0]))
    stock_values.append(int(stock_close.get(0, 0)))

    csv_obj.append(stock_values)
    
    print(csv_obj)

# return csv_obj

def main():

    # 1. get the dates for which data is required
    datesDataFrame = get_dates_v2()

    # 2. get the final data obj
    csv_obj = get_stock_data(datesDataFrame)

    # 3. write to csv
    # write_to_csv(csv_obj, datetime.date.today().strftime('%Y-%b-%d')+"-v2.tsv")


# if __name__ == '__main__':
#     main()

# arr = [['a', 10, 11, 12, 13], 
#        ['b', 20, 21, 22, 23], 
#        ['c', 30, 31, 32, 33]]

# for tr in range(len(arr[0])-1):
#     dictionary = {x[0]: x[tr+1] for x in arr}
#     print(dictionary)
#     print(sorted(dictionary, reverse=True))
#     print('==================')

df = pd.read_excel('./data.xlsx')



tr=0
d = dict()
finaldict = dict()

for colidx in range(len(df.columns)-1):
    print('Processing for: ' + df.columns[colidx+1])

    colname = df.columns[colidx+1]

    for idx in range(len(df.get('Share'))):
        
        # below line do only 1
        if colidx == 0:
            finaldict[df.get('Share')[idx]] = 0

        d[df.get('Share')[idx]] = df.get(colname)[idx]

    sorted_d = sorted(d.items(), key=lambda x:x[1], reverse=True)

    # print(finaldict)

    print(sorted_d)

    for i in range(len(sorted_d)):
        # print(f'{i+1} {sorted_d[i][0]}')
        # add this score to finaldict
        finaldict[sorted_d[i][0]] = finaldict[sorted_d[i][0]] + i+1

# print(finaldict)
finaldict = sorted(finaldict.items(), key=lambda x:x[1])
print(finaldict)
write_to_xls(finaldict, "ranking")