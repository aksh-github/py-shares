

import datetime
import yfinance as yf
import pandas as pd
import csv

def get_dates():

    stock = yf.Ticker("SBIN.BO")

    date_range = ["5y", "1y", "6mo", "3mo", "1mo", "5d", "1d"]
    start_dates = []
    end_dates = []

    df = stock.history(period=date_range[0], actions=False, rounding=True)
    start_dates.append(df.index[0].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    df = stock.history(period=date_range[1], actions=False, rounding=True)
    start_dates.append(df.index[0].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    df = stock.history(period=date_range[2], actions=False, rounding=True)
    start_dates.append(df.index[0].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    df = stock.history(period=date_range[3], actions=False, rounding=True)
    start_dates.append(df.index[0].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    df = stock.history(period=date_range[4], actions=False, rounding=True)
    start_dates.append(df.index[0].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))


    df = stock.history(period=date_range[5], actions=False, rounding=True)
    start_dates.append(df.index[0].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    # today
    df = stock.history(period=date_range[6], actions=False, rounding=True)
    start_dates.append(df.index[0].strftime("%Y-%m-%d"))
    end_dates.append(None)


    # print(start_dates, end_dates)

    df = pd.DataFrame({
        'start_date': start_dates,
        'end_date': end_dates
    })

    # print(df)

    return df

# call the function
# print(get_dates())

def printmy(data):
    print(data)

# print(datetime.date.today().strftime('%Y-%b-%d'))