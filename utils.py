

import datetime
from datetime import date, timedelta
import yfinance as yf
from yahooquery import Ticker
import pandas as pd
import csv
import xlsxwriter
import uuid


def get_dates():

    stock = yf.Ticker("HINDUNILVR.NS")

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


def get_dates_v2_new():
    
    # date_range = ["5y", "2y", "1y", "6mo", "3mo", "1mo", "5d", "1d"]
    date_range = [365*5, 365*2, 365*1, 181, 90, 30, 5, 0]
    start_dates = []
    end_dates = []

    current_date = date.today()

    for noOfDays in date_range:
        back_date = current_date - timedelta(days=noOfDays)
        start_dates.append(back_date.strftime("%Y-%m-%d"))
        end_dates.append((back_date - timedelta(days=1)).strftime("%Y-%m-%d"))

    df = pd.DataFrame({
        'start_date': start_dates,
        'end_date': end_dates
    })

    print(df)

    return df


def getDatesWithDiff(diff):
    # Get today's date
    today = date.today()
    one_year_back = today - timedelta(days=diff)

    # print("Today's date:", today.strftime("%Y-%m-%d"))
    # print("Date one year back:", one_year_back.strftime("%Y-%m-%d"))

    return [today.strftime("%Y-%m-%d"), one_year_back.strftime("%Y-%m-%d")]

def get_dates_v2():

    stock = Ticker("HINDUNILVR.NS")

    date_range = ["5y", "2y", "1y", "6mo", "3mo", "1mo", "5d", "1d"]
    start_dates = []
    end_dates = []

    idx = 0

    df = stock.history(period=date_range[idx])
    # print(df)
    # print(df.index[0][1], df.index[0][1].strftime("%Y-%m-%d"))
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))


    idx = idx + 1
    df = stock.history(period=date_range[idx])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    idx = idx + 1
    df = stock.history(period=date_range[idx])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    idx = idx + 1
    df = stock.history(period=date_range[idx])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    idx = idx + 1
    df = stock.history(period=date_range[idx])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))


    idx = idx + 1
    df = stock.history(period=date_range[idx])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))


    idx = idx + 1
    df = stock.history(period=date_range[idx])
    start_dates.append(df.index[0][1].strftime("%Y-%m-%d"))
    end_dates.append((df.index[0][1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))


    # # today
    idx = idx + 1
    df = stock.history(period=date_range[idx])
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


def write_to_xls(data, filename):
    workbook = xlsxwriter.Workbook(filename='./output/' + filename + '-' + str(uuid.uuid4())[:8] + ".xlsx")
    worksheet = workbook.add_worksheet()

    row = 0

    for i in range(len(data)):
        col = 0
        for j in range(len(data[i])):
                # print(data[i][j])
            worksheet.write(row, col, data[i][j])
            col = col + 1
        row = row + 1

    workbook.close()