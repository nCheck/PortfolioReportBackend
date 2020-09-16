from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData , create_engine , Table, Column, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP , FLOAT , DATETIME
from dbconnect import getEngine

Base = declarative_base()

class BondDescrp(Base):
   __tablename__ = 'bondDescrp'
   
   bdid = Column(Integer, primary_key = True)
   isin = Column( String(100) )
   category = Column(String(100))
   bondName = Column(String(100))
   parValue = Column( FLOAT )
   coupon = Column( FLOAT )
   issueDate = Column( DATETIME )
   maturityDate = Column( DATETIME )
   tenure = Column( FLOAT )




Base.metadata.create_all( getEngine() )

Base = declarative_base()

class CurrentPortfolio(Base):
   __tablename__ = 'currentPorfolio'
   
   cpid = Column(Integer, primary_key = True)
   typeOfInstrument = Column( String(255) )
   isin = Column( String(100) )
   ticker = Column( String(100) )
   quantity = Column( FLOAT )
   clientId = Column(String(100))
   averagePrice = Column( FLOAT(precision=2) )



Base.metadata.create_all( getEngine() )


Base = declarative_base()

class PortfolioHistory(Base):
   __tablename__ = 'portfolioHistory'
   
   phid = Column(Integer, primary_key = True)
   clientId = Column(String(100))
   totalInvested = Column( FLOAT(precision=2) )
   netPosition = Column( FLOAT(precision=2) )
   date = Column( DATETIME )


   def __str__(self):
       return f'{self.date} { self.totalInvested}'




Base.metadata.create_all( getEngine() )



Base = declarative_base()

class StockDescrp(Base):
   __tablename__ = 'stockDescrp'
   
   sdid = Column(Integer, primary_key = True)
   isin = Column( String(100) )
   sector = Column(String(100))
   stockName = Column(String(100))
   ticker = Column(String(100))
   marketValuation = Column(String(100))



Base.metadata.create_all( getEngine() )


Base = declarative_base()

class Transactions(Base):
   __tablename__ = 'transactions'
   
   tid = Column(Integer, primary_key = True)
   clientId = Column(String(100))
   typeOfInstrument = Column( String(255) )
   isin = Column( String(100) )
   ticker = Column( String(100) )
   quantity = Column( FLOAT )
   price = Column( FLOAT )
   timestamp = Column( DATETIME )
   settleDate = Column( DATETIME )
   brokerCode = Column( String(100) )
   action = Column( String(100) )


   def __str__(self):
       return self.ticker + " " + str(self.quantity) + " " + str( self.price ) + " " + str( self.timestamp ) + " " + self.action



Base.metadata.create_all( getEngine() )