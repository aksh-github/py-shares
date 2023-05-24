
#https://finance.yahoo.com/quote/INFY.BO/history?period1=1653372093&period2=1684908093&interval=capitalGain%7Cdiv%7Csplit&filter=capitalGain&frequency=1d&includeAdjustedClose=true
#https://pypi.org/project/yfinance/

import yfinance as yf
import pandas as pd
import numpy as np


# input, read csv

df = pd.read_csv('input.csv')

# print(df)

for idx, s in enumerate(df.get('Shares')):
    # print(s)
    msft = yf.Ticker(s+".BO")
    df = msft.history(period="5d", actions=False, rounding=True)
    print(df)
    # print(df['Close'].size)
    stock_close = df['Close']
    # stock_date = df['Date']
    if 0==idx:
        print("Got updated on: ", df.index[0])

    # print(df.index, stock_close[0])
    print(s+".BO ",stock_close[0])
    print('====================')



# correct
# shares = ["TCS", "WIPRO"]
# for s in shares:
#     msft = yf.Ticker(s+".BO")
#     df = msft.history(period="1d")
#     print(s+".BO", df['Close'][0])


# msft = yf.Ticker("HCLTECH.BO")
# d1 = msft.history(period="1d")
# print(d1)   # works

# df = pd.DataFrame(d1)

# print(d1['Close'], df.get('Close'))   # works

# print(d1)

# print(d1['Close'][0], d1.get('Close')[0])   # gives final val perfect

# print(df.to_json("./tp.json"))  # works


