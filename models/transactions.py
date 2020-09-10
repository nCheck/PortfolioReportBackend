from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData , create_engine , Table, Column, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP , FLOAT , DATETIME


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



# from dbconnect import getEngine
# Base.metadata.create_all( getEngine() )