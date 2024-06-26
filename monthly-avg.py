
from yahooquery import Ticker
import pandas as pd
from utils import get_dates_v2, getDatesWithDiff, write_to_xls
from datetime import date, timedelta
import matplotlib.pyplot as plt

# all abt pandas: https://www.youtube.com/watch?v=DkjCaAMBGWM&t=57s

def dumData():
    pdf = pd.read_excel('./output/year-data-avg.xlsx')

    # print(pdf['close'].size)
    # # print(pdf['symbol'][0])

    # #share name
    # sym = pdf['symbol']
    # # sym = pdf.index.get_level_values(0)[0]
    # print(sym, pdf.describe(), )

    plt.plot(pdf.date, pdf.close)
    plt.show()


def processData(pdf=None, rowIdx=0):
    # pdf = pd.read_excel('./output/year-data-avg.xlsx')

    # print(pdf['close'].size)
    # print(pdf['symbol'][0])

    #share name
    # sym = pdf['symbol']
    sym = pdf.index.get_level_values(0)[0]
    # print(sym)


    curMon = -1
    sum = 0
    ctr=0
    year_data=[]
    if(rowIdx==0):
        year_data.append(['Share', ""])
    # first_row = ['Share', ""]
    data_row=[sym, ""]
    # year_data.append([sym])
    for idx in range(len(pdf['close'])):
        # print(pdf.index.get_level_values(1)[idx].strftime('%b'), pdf['close'][idx])
        # print(pdf['date'][idx].strftime('%b'), pdf['close'][idx])
        # mon = pdf['date'][idx].strftime('%b')   
        mon = pdf.index.get_level_values(1)[idx].strftime('%b')
        
        if(curMon!=mon):
            if(curMon!=-1):
                # print(curMon, ctr, sum)
                if(rowIdx==0):
                    year = pdf.index.get_level_values(1)[idx].strftime('%y')
                    year_data[rowIdx].append(curMon + '-' + year)
                # print("avg for", curMon, sum/ctr)
                data_row.append(int(sum/ctr))
            

            #reset
            sum=0
            ctr=0
            # start new calc
            curMon=mon
            ctr+=1
            sum += pdf['close'][idx]
        else:
            ctr+=1
            sum += pdf['close'][idx]
            # print(sum)

    # last month
    # print(curMon, ctr, sum)
    # print("avg for", curMon, sum/ctr)
    if(rowIdx==0):
        year_data[rowIdx].append(curMon + '-' + year)

    data_row.append(int(sum/ctr))   # append avg values
    year_data.append(data_row)      # append all values for share

    # print(len(year_data), year_data)
    return year_data



def generateData(stock: Ticker, startDate=365, endDate=0 ):
    
    # df = stock.history(start=startDate, end=endDate)
    df = stock.history(period='1y')
    # head = df.head()
    # print(head)
    
    stock_close = df['close']
    # print(df.index[0])
    # print(stock_close.head())

# this is panda df
    pdf = pd.DataFrame(stock_close)
    
    # print(pdf.columns)
    # print('====================')
    # pdfhead = pdf.head()
    # print(pdfhead['close'].size)
    # print('====================')
    # print(pdfhead.index.get_level_values(1)[0].strftime('%b'))


    # print(pdf.iterrows())
    # print('====================', len(pdfhead.index.get_level_values(1)))

    # for row in pdf['close']:
    #     print(row)
        
    
    # return stock_close
    return pdf


def iterateInput(filedf):
    all_data=[]
    for idx, share in enumerate(filedf.get('Shares')):
    #for x in range(2):
        print("processing...", share)
        stock = Ticker(share+".NS")
        pdf = generateData(stock)
        year_data = processData(pdf, idx)
        # print()
        for y in range(len(year_data)):
            all_data.append(year_data[y])
            if(idx!=0):
                print(all_data)
    return all_data


def perc_calc(arr2d):
    # percdf = pd.DataFrame()
    arr2d[0][0] = 'Month'
    print(arr2d[0][0])
    perc_data={}
    # arr2d = [
    #     ['HDFCBANK.NS', '', 1656, 1672, 1609, 1585, 1514, 1506, 1652, 1582, 1421, 1443, 1514, 1488, 1587], 
    #          ['zodiac.NS', '', 133, 124, 124, 130, 144, 153, 162, 282, 288, 387, 467, 621, 620]]
    
    # print(len(arr2d[0][3:]))    # 13
    # print(arr2d[0][3:])

    for idx in range(len(arr2d)):
        # print(arr2d[idx])

        to_skip = 2
        perc_data[arr2d[idx][0]] = arr2d[idx][to_skip:]
        stok = perc_data[arr2d[idx][0]]
        # print(stok)
        if(idx!=0):
            for j in range(len(stok)):
                if(j+1 < len(stok)):
                    perc = (stok[j+1] / stok[j] * 100) - 100
                    stok[j] = round(perc, 2)

    # print(perc_data)
    percdf = pd.DataFrame(perc_data)[:-1]
    print(percdf)
    return percdf

    
def plot_perc(percdf):

    for idx in range(len(percdf.columns)):
        if(idx!=0):
            print(percdf.columns[idx])
            plt.plot(percdf.Month, percdf[percdf.columns[idx]], label=percdf.columns[idx])
            plt.plot()

    plt.legend()
    plt.ylabel("% change")
    plt.xlabel("Time")
    plt.grid()
    plt.show()

def main():

    # pdfhead.to_excel('./output/year-data.xlsx')

# 1. read share names
    filedf = pd.read_csv('input.csv')

    # print(df)

# 2. iterate over each and process
    all_data = iterateInput(filedf)
    # print(all_data)

# 3. write final data to excel
    write_to_xls(all_data, "monthly-average")

    # dumData()

# 4. calculate %
    percdf = perc_calc(all_data)

# 5. plot graph
    plot_perc(percdf)


if __name__ == '__main__':
    main()