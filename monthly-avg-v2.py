#!/usr/bin/env python
# coding: utf-8

from yahooquery import Ticker
import pandas as pd
from pandasgui import show
import datetime
import time
import matplotlib.pyplot as plt

from utils import write_to_xls

def get_hist(stockname):

    stock = Ticker(stockname)
    df = stock.history(period='1y')
    stock_close = df['close']
    pdf = pd.DataFrame(stock_close)

    # pdf
    # show(pdf)

    pdf = pdf.reset_index()
    # show(pdf)

    # pdf['MonYr'] = pdf['date'].map(lambda x: str(x.year) + '-' + str(x.month))
    pdf['MonYr'] = pdf['date'].map(lambda x: x.strftime('%b') + '-' + x.strftime('%y'))
    pdf['uxts'] = pdf['date'].map(lambda x: int(time.mktime(datetime.date(x.year, x.month, 1).timetuple())))
    # pdf
    #show(pdf)

    return pdf


def calculate(pdf):
    avgdf = pdf[['uxts', 'MonYr', 'symbol', 'close']].groupby(['uxts', 'MonYr', 'symbol']).agg(sum=('close', 'sum'), count=('close', 'size'), max=('close', 'max'))
    # show(avgdf)

    avgdf['avg'] = avgdf['sum'] / avgdf['count']
    # avgdf
    # show(avgdf)

# calculate the %change in consecutive values
    avgdf['LastChange'] = avgdf['avg'] / avgdf['avg'].shift(1)
    # set value to 0 rather than something as NaN
    avgdf['LastChange'].values[0] = 0

# calculate the %change in 1st to all other values
    avgdf['OverallChange'] = avgdf['avg'] / avgdf['avg'].values[0]
    # avgdf
    # show(avgdf)
    return avgdf

def plot_perc(percdf):

    for idx in range(len(percdf.columns)):
        if(idx!=0):
            print(percdf.columns[idx])
            plt.plot(percdf['MonYr'], percdf[percdf.columns[idx]], label=percdf.columns[idx])
            plt.plot()

    plt.legend()
    plt.ylabel("% change")
    plt.xlabel("Time")
    plt.grid()
    plt.show()

def iterateInput(filedf):
    chgdf = pd.DataFrame({'MonYr': []})
    all_data=[]
    all_data.append(['share', ''])
    for idx, share in enumerate(filedf.get('Shares')):
    #for x in range(2):
        print("processing...", share)
        pdf = get_hist(share)
        avgdf = calculate(pdf)
        avgdf = avgdf.reset_index()
        # print(len(avgdf))
        if(idx==0):
            # show(avgdf)
            # print(idx)
            for j, month in enumerate(avgdf['MonYr']):
                # print(j, month)
                all_data[0].append(month)
                # chgdf['MonYr']
            chgdf['MonYr'] = avgdf['MonYr'][1:]     #skip 1st because its 0

        rowOfAvg = []
        rowOfMax = []
        rowOfChg = []
        for j, month in enumerate(avgdf['avg']):
            if(j==0):
                rowOfAvg.append(avgdf['symbol'].values[0])
                rowOfAvg.append("")
            rowOfAvg.append(int(avgdf['avg'].values[j]))
            rowOfMax.append(int(avgdf['max'].values[j]))
            rowOfChg.append(avgdf['LastChange'].values[j]*100-100)

        rowOfAvg.append("")     #empty col

# create single row for avg n max
        all_data.append([*rowOfAvg, *rowOfMax])

        # chgdf
        chgdf[avgdf['symbol'].values[0]] = rowOfChg[1:]     #skip 1st because its 0
        

    # show(chgdf)

    return all_data, chgdf


def main():
    # 1. read share names
    filedf = pd.read_csv('input.csv')
    # print(filedf)

    # 2. iterate over each and process
    all_data, chgdf = iterateInput(filedf)

    # 3. write final data to excel
    # print(all_data)
    write_to_xls(all_data, "monthly-average-v2")

# 4. plot graph
    plot_perc(chgdf)

if __name__ == '__main__':
    main()