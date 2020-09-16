from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData , create_engine , Table, Column, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP , FLOAT , DATETIME


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



# from dbconnect import getEngine
# Base.metadata.create_all( getEngine() )