#custom
from models.stockDescrp import StockDescrp
from models.dbconnect import getEngine
from ltp import lastTradedPrice , getISIN

#inbuilt
from sqlalchemy.orm import sessionmaker
import datetime
from random import randint
import pandas as pd

df = pd.read_csv('dataset/stockdescrp.csv')


engine = getEngine()
Session = sessionmaker(bind = engine)
session = Session()




def loadStockDescrp():

    stocks = []
    for index, row in df.iterrows():
        isin = row['isin']
        sector = row['sector']
        stockName = row['stockName']
        ticker = row['ticker']
        marketValuation = row['marketValuation']


        sd = StockDescrp(isin=isin , sector=sector, stockName=stockName, ticker=ticker,
                        marketValuation=marketValuation)

        stocks.append(sd)

    
    session.add_all(stocks)
    session.commit()




loadStockDescrp()