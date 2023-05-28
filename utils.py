

import datetime
import yfinance as yf
from yahooquery import Ticker
import pandas as pd
import csv

def get_dates():

    stock = yf.Ticker("INFY.BO")

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


def get_dates_v2():

    stock = Ticker("TECHM.BO")

    date_range = ["5y", "1y", "6mo", "3mo", "1mo", "5d", "1d"]
    start_dates = []
    end_dates = []

    df = stock.history(period=date_range[0])
    # print(df)
    # print(df.index[0][1], df.index[0][1].strftime("%Y-%m-%d"))
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    df = stock.history(period=date_range[1])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    df = stock.history(period=date_range[2])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    df = stock.history(period=date_range[3])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    df = stock.history(period=date_range[4])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))


    df = stock.history(period=date_range[5])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    # # today
    df = stock.history(period=date_range[6])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append(None)


    # print(start_dates, end_dates)

    df = pd.DataFrame({
        'start_date': start_dates,
        'end_date': end_dates
    })

    # print(df)

    return df

def write_to_csv(data, filename):
    
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(data)
# print(datetime.date.today().strftime('%Y-%b-%d'))