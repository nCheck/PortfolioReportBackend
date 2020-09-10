#custom
from models.transactions import Transactions
from models.currentPortfolio import CurrentPortfolio
from models.portfolioHistory import PortfolioHistory
from models.dbconnect import getEngine

#inbuilt
from sqlalchemy.orm import sessionmaker
import datetime

engine = getEngine()
Session = sessionmaker(bind = engine)
session = Session()

#insert one data
def test():
    
    cp = PortfolioHistory( clientId = 'J001' , totalInvested = 785.1
            , netPosition = 800.5 , date = datetime.datetime.now() )

    session.add(cp)
    session.commit()


#insert bulk data
def insertTransaction():

    trans = []

    for i in range(1,5):

        t = Transactions( clientId = 'J001' , typeOfInstrument = 'STOCK'
                    , isin='5001' , ticker='AAPL' , quantity=(i+2) , price=(100+i)
                    , timestamp= datetime.datetime.now() )
        
        trans.append(t)

    session.add_all(trans)

    session.commit()


