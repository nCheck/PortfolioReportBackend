from random import randint
from datetime import datetime , timedelta
import pandas as pd

npd = pd.read_csv('dataset/realval.csv')
npd['timestamp'] = pd.to_datetime(npd['timestamp'])




BONDS = [ 'MUFG/22', 'GT10:GOV' , 'ACC24' , 'GT5:GOV' , 'SYY22' , 'GTII10:GOV' ]

def isBond( name ):

    if name in BONDS:
        return True
    else:
        return False

def lastTradedPrice(stock , curPrice=0.0 , date = datetime.now() , type = 'BOND'):



    if isBond(stock):

        vals = [ 5 , 10 , -5 , -10 , -2 , 2 ]
        rn = randint(1,40) % len(vals)
        return curPrice + vals[rn]

    else:

        f1 = npd[npd['timestamp'] == date ]
        
        if len(f1) == 0:
            date = date + timedelta(days=2)
            f1 = npd[npd['timestamp'] == date ]
        
        if len(f1) == 0:
            return curPrice + 5
        else:
            return float(f1[ npd['ticker'] == stock ].Close)



def getISIN(stock):

    isinlist = {'TSLA':'US88160R1014',
    'BAC':'US0605051046',
    'BA':'US0970231058',
    'KO':'US1912161007',
    'AMZN':'US0231351067',
    'NFLX':'US64110L1061',
    'MUFG/22': 'US-000402625-0' ,
    'GT10:GOV': 'US-000406665-0' ,
    'ACC24': 'US-000409925-0',
    'GT5:GOV': 'US-000202625-0',
    'SYY22': 'US-000333625-0',
    'GTII10:GOV': 'US-000802625-0'
    }

    return isinlist[stock]



# print(lastTradedPrice('KO' , 0,  datetime(2019, 1, 2, 0, 0)))