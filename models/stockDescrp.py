from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData , create_engine , Table, Column, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP , FLOAT , DATETIME


Base = declarative_base()

class StockDescrp(Base):
   __tablename__ = 'stockDescrp'
   
   sdid = Column(Integer, primary_key = True)
   isin = Column( String(100) )
   sector = Column(String(100))
   stockName = Column(String(100))
   ticker = Column(String(100))
   marketValuation = Column(String(100))



# from dbconnect import getEngine
# Base.metadata.create_all( getEngine() )