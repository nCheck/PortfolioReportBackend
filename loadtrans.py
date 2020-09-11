#custom
from models.transactions import Transactions
from models.currentPortfolio import CurrentPortfolio
from models.portfolioHistory import PortfolioHistory
from models.dbconnect import getEngine
from ltp import lastTradedPrice , getISIN

#inbuilt
from sqlalchemy.orm import sessionmaker
import datetime
from random import randint
import pandas as pd

df = pd.read_csv('dataset/stockdata.csv')


engine = getEngine()
Session = sessionmaker(bind = engine)
session = Session()



def loadtrans():

    trans = []
    for index, row in df.iterrows():

        clientId = 'J001'
        typeOfInstrument = 'STOCK'
        action = str(row['action']).upper()
        ticker = str(row['ticker']).upper()

        quantity = row['quantity']
        price = row['price']
        timestamp = datetime.datetime.strptime( row['timestamp'] , '%m/%d/%Y')
        brockerCode = row['brockerCode']

        t = Transactions( clientId = clientId , typeOfInstrument = typeOfInstrument , action = action
                    , isin=getISIN(ticker) , ticker=ticker, quantity=quantity , price=price
                    , timestamp=timestamp , brokerCode=brockerCode )

        trans.append(t)




    session.add_all(trans)

    session.commit()

loadtrans()


def getDates():
    dates = session.query(Transactions.timestamp).filter(Transactions.typeOfInstrument == 'STOCK').distinct()
    for d in dates:
        print(d)


# getDates()