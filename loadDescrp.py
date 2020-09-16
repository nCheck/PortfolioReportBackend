#custom
from models.bondDescrp import BondDescrp
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

bf = pd.read_csv('dataset/bonddescrp.csv')

def loadBondDescrp():

    bonds = []
    for index, row in bf.iterrows():
        isin = row['isin']
        category = row['category']
        bondName = row['bondName']
        coupon = row['coupon']
        parValue = row['parValue']
        issueDate = datetime.datetime.strptime( row['issueDate'] , '%Y-%m-%d')  
        maturityDate =  datetime.datetime.strptime( row['maturityDate'] , '%Y-%m-%d') 
        tenure = row['Tenure']






        bd = BondDescrp(isin=isin , category=category, bondName=bondName, coupon=coupon,
                        parValue=parValue, issueDate=issueDate, maturityDate=maturityDate , tenure=tenure)

        bonds.append(bd)

    
    session.add_all(bonds)
    session.commit()


loadBondDescrp()