from random import randint


def lastTradedPrice(stock , curPrice=0.0):

    chngs = [ -20.0 , -10.0 , 3.0 , 4.0 , 10.0 , 25.0 , 60.0 , -50.0 ]
    n = len(chngs)
    dif = chngs[ randint(1,55477) % n ]

    return curPrice + dif



def getISIN(stock):

    isinlist = {'TSLA':'US88160R1014',
    'BAC':'US0605051046',
    'BA':'US0970231058',
    'KO':'US1912161007',
    'AMZN':'US0231351067',
    'NFLX':'US64110L1061'}

    return isinlist[stock]


