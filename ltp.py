from random import randint
from datetime import datetime , timedelta
import pandas as pd
import requests, json

npd = pd.read_csv('dataset/realval.csv')
npd['timestamp'] = pd.to_datetime(npd['timestamp'])




TICKER_CACHE = {}

def getPrice(ticker):

    if ticker in TICKER_CACHE.keys():
        return TICKER_CACHE[ticker]

    headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token 24bc8b2483ff559f1ce6e535b5a7be14f44ef50e'
        }
    url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices'
    requestResponse = requests.get(url, headers=headers)

    TICKER_CACHE[ticker] = (requestResponse.json())[0]['close']

    return TICKER_CACHE[ticker]

#stub
def getStockSector(stock):

    if isBond(stock):
        return "Government"


    sec_stoc = {"TSLA": "Auto Manufacturers","BAC": "Finance","BA": "Aerospace" ,
    "KO": "Beverage","AMZN": "Internet Retail", "NFLX": "Entertainment"}

    return sec_stoc[stock]

BONDS = [ 'MUFG/22', 'GT10:GOV' , 'ACC24' , 'GT5:GOV' , 'SYY22' , 'GTII10:GOV' ]

def isBond( name ):

    if name in BONDS:
        return True
    else:
        return False

def lastTradedPrice(stock , curPrice=0.0 , date = datetime.now() , type = 'BOND'):

    # print(stock , date , curPrice)

    if isBond(stock):

        vals = [ 5 , 3 , 10 , -1 , -2 , 2 ]
        rn = randint(1,40) % len(vals)
        return curPrice + vals[rn]

    else:

        f1 = npd[npd['timestamp'] == date ]
        
        print(f1[ npd['ticker'] == stock ].size, stock , "Sizee")


        for i in range(1,10):

            f1 = npd[npd['timestamp'] == date ]
            if f1.size == 0:
                date = date + timedelta(days=i)
            else:
                break
                
        
        if f1.size == 0:
            return getPrice(stock)
        else:
            # print(f1.head() , stock)
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