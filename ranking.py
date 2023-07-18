
import datetime
import pandas as pd
from utils import write_to_xls

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
write_to_xls(finaldict, "ranking-"+ datetime.date.today().strftime('%Y-%b-%d'))