from random import randint
from datetime import datetime
import pandas as pd

npd = pd.read_csv('dataset/realval.csv')
npd['timestamp'] = pd.to_datetime(npd['timestamp'])

def lastTradedPrice(stock , curPrice=0.0 , date = datetime.now()):

    date = date[0]
    # print(stock , date )

    f1 = npd[npd['timestamp'] == date ]
    
    return float(f1[ npd['ticker'] == stock ].Close)



def getISIN(stock):

    isinlist = {'TSLA':'US88160R1014',
    'BAC':'US0605051046',
    'BA':'US0970231058',
    'KO':'US1912161007',
    'AMZN':'US0231351067',
    'NFLX':'US64110L1061'}

    return isinlist[stock]



# print(lastTradedPrice('KO' , 0,  datetime(2019, 1, 2, 0, 0)))