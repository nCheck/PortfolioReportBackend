from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData , create_engine , Table, Column, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP , FLOAT , DATETIME



Base = declarative_base()

class CurrentPortfolio(Base):
   __tablename__ = 'currentPorfolio'
   
   cpid = Column(Integer, primary_key = True)
   typeOfInstrument = Column( String(255) )
   isin = Column( String(100) )
   ticker = Column( String(100) )
   quantity = Column( FLOAT )
   clientId = Column(String(100))
   averagePrice = Column( FLOAT )



# from dbconnect import getEngine
# Base.metadata.create_all( getEngine() )