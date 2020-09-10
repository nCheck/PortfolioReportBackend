from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData , create_engine , Table, Column, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP , FLOAT , DATETIME




Base = declarative_base()

class PortfolioHistory(Base):
   __tablename__ = 'portfolioHistory'
   
   phid = Column(Integer, primary_key = True)
   clientId = Column(String(100))
   totalInvested = Column( FLOAT )
   netPosition = Column( FLOAT )
   date = Column( DATETIME )

   def __str__(self):
       return f'{self.date} { self.totalInvested}'



# from dbconnect import getEngine
# Base.metadata.create_all( getEngine() )