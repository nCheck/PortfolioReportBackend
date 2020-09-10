from random import randint


def lastTradedPrice(stock , curPrice=0.0):

    chngs = [ -20.0 , -10.0 , 3.0 , 4.0 , 10.0 , 25.0 , 60.0 , -50.0 , 100.0 ]
    n = len(chngs)
    dif = chngs[ randint(1,55477) % n ]

    return curPrice + dif

