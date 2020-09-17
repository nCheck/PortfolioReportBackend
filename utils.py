import flask
import os
from flask import jsonify, request
from flask import flash, redirect, url_for, session
from flask_cors import CORS, cross_origin
import requests, json
import pandas as pd
import random


#custom

#orm models
from models.transactions import Transactions
from models.currentPortfolio import CurrentPortfolio
from models.portfolioHistory import PortfolioHistory
from models.dbconnect import getEngine
from models.stockDescrp import StockDescrp
from models.bondDescrp import BondDescrp

from ltp import lastTradedPrice , getISIN

#inbuilt
from sqlalchemy.orm import sessionmaker
import datetime
from random import randint

engine = getEngine()
Session = sessionmaker(bind = engine)
session = Session()


TICKER_CACHE = {}

def getPrice(ticker):

    if ticker in TICKER_CACHE.keys():
        return TICKER_CACHE[ticker]

    headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token 24bc8b2483ff559f1ce6e535b5a7be14f44ef50e'
        }
    url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices'
    requestResponse = requests.get(url, headers=headers)

    TICKER_CACHE[ticker] = (requestResponse.json())[0]['close']

    return TICKER_CACHE[ticker]

def topthreecards():
    stocks = session.query(CurrentPortfolio).filter(CurrentPortfolio.typeOfInstrument == 'STOCK')
    total_stock_valuation = 0
    total_investment = 0
    max_unrealized_pl = 0
    max_gainer = ''
    min_unrealized_pl = 9999999
    max_loser = ''
    for row in stocks:
        current_market_price = (getPrice(str(row.ticker)))
        quantity = int(row.quantity)
        total_stock_valuation = total_stock_valuation+(current_market_price*quantity)
        total_investment = total_investment+(row.averagePrice*quantity)
        unrealized_pl = total_stock_valuation-total_investment
        if unrealized_pl>max_unrealized_pl:
            max_unrealized_pl = unrealized_pl
            max_gainer = session.query(StockDescrp.stockName).filter(StockDescrp.isin==row.isin).one()[0]
        if unrealized_pl<min_unrealized_pl:
            min_unrealized_pl = unrealized_pl
            max_loser = session.query(StockDescrp.stockName).filter(StockDescrp.isin==row.isin).one()[0]
    bonds = session.query(CurrentPortfolio).filter(CurrentPortfolio.typeOfInstrument == 'BOND')
    total_bond_valuation = 0
    for row in bonds:
        current_market_price = row.averagePrice+random.randrange(-10, 10, 1)
        # current_market_price = lastTradedPrice( row.ticker , row.averagePrice )
        quantity = int(row.quantity)
        total_bond_valuation = total_bond_valuation+current_market_price*quantity
        total_investment = total_investment+(row.averagePrice*quantity)
        unrealized_pl = total_bond_valuation-total_investment
        if unrealized_pl>max_unrealized_pl:
            max_unrealized_pl = unrealized_pl
            max_gainer = session.query(BondDescrp.bondName).filter(BondDescrp.isin==row.isin).one()[0]
        if unrealized_pl<min_unrealized_pl:
            min_unrealized_pl = unrealized_pl
            max_loser = session.query(BondDescrp.bondName).filter(BondDescrp.isin==row.isin).one()[0]
    total_valuation = total_stock_valuation+total_bond_valuation
    total_unrealized_pl = total_valuation-total_investment
    total_pl_percentage = (total_unrealized_pl/total_investment)*100
    res = {'card1':{'field1': 'My investment','value1': total_investment, 'field2' :'My networth','value2':total_valuation},'card2':{'field1': 'Total Profit&Loss','value1': total_unrealized_pl,'field2': 'Total Profit&Loss%','value2': total_pl_percentage},'card3':{'field1': 'Max Gainer','value1': max_gainer,'field2': 'Max Loser','value2': max_loser}}
    return (res)


def securitydistgraph():
    stocks = session.query(CurrentPortfolio).filter(CurrentPortfolio.typeOfInstrument == 'STOCK')
    total_stock_valuation = 0
    for row in stocks:
        current_market_price = (getPrice(str(row.ticker)))
        quantity = int(row.quantity)
        total_stock_valuation = total_stock_valuation+(current_market_price*quantity)
    bonds = session.query(CurrentPortfolio).filter(CurrentPortfolio.typeOfInstrument == 'BOND')
    total_bond_valuation = 0
    for row in bonds:
        current_market_price = row.averagePrice+random.randrange(-10, 10, 1)
        quantity = int(row.quantity)
        total_bond_valuation = total_bond_valuation+current_market_price*quantity
    stock_percentage = total_stock_valuation/(total_stock_valuation+total_bond_valuation)
    bond_percentage = 1-stock_percentage
    res = { 'labels':['Stocks','Bonds'],'datasets':[stock_percentage*100,bond_percentage*100]}
    return ( res )

def sectordistgraph():
    sector_summary = {}
    stock_details = session.query(StockDescrp)
    bond_details = session.query(BondDescrp)
    total_value = 0
    sector_labels = []
    sector_percentage = []
    for row in stock_details:

        try :
            quantity = int(session.query(CurrentPortfolio.quantity).filter(CurrentPortfolio.isin==row.isin).one()[0] )
            if row.sector in sector_summary.keys():
                stock_valuation = getPrice(str(row.ticker))*quantity
                updated_value = sector_summary[row.sector]+stock_valuation
                sector_summary[row.sector] = updated_value
            else:
                stock_valuation = getPrice(str(row.ticker))*quantity
                sector_summary[row.sector] = stock_valuation
            total_value = total_value+stock_valuation

        except :
            pass

    for row in bond_details:

        try :
            quantity = int(session.query(CurrentPortfolio.quantity).filter(CurrentPortfolio.isin==row.isin).one()[0])
            if row.category in sector_summary.keys():
                bond_valuation = (row.parValue+random.randrange(-10, 10, 1))*quantity
                updated_value = sector_summary[row.category]+bond_valuation
                sector_summary[row.category] = updated_value
            else:
                bond_valuation = (row.parValue+random.randrange(-10, 10, 1))*quantity
                sector_summary[row.category] = bond_valuation
            total_value = total_value+bond_valuation
        except :
            pass

    for key in sector_summary.keys():
        sector_labels.append(key)
        sector_percentage.append((sector_summary[key]/total_value)*100)
    res = { 'labels':sector_labels,'datasets':[{'data': sector_percentage}]}
    return ( res )

def tabledata():
    stocks = session.query(CurrentPortfolio).filter(CurrentPortfolio.typeOfInstrument == 'STOCK')
    total_stock_valuation = 0
    total_stock_investment = 0
    stock_details_data = []
    total_stock_unrealized_pl = 0
    for row in stocks:
        current_market_price = (getPrice(str(row.ticker)))
        quantity = int(row.quantity)
        current_valuation = current_market_price*quantity
        total_stock_valuation = total_stock_valuation+current_valuation
        current_investment = row.averagePrice*quantity
        total_stock_investment = total_stock_investment+current_investment
        unrealized_PL = current_valuation-current_investment
        total_stock_unrealized_pl = total_stock_unrealized_pl+unrealized_PL
        stockName = session.query(StockDescrp.stockName).filter(StockDescrp.isin==row.isin).one()[0]
        stock_details_data.append({'name': stockName, 'quantity': quantity, 'investment': current_investment,
                                    'ticker' : row.ticker  ,'currentValuation': current_valuation, 'unrealizedPL': unrealized_PL })
    bonds = session.query(CurrentPortfolio).filter(CurrentPortfolio.typeOfInstrument == 'BOND')
    total_bond_valuation = 0
    total_bond_investment = 0
    bond_details_data = []
    total_bond_unrealized_pl = 0
    for row in bonds:
        current_market_price = row.averagePrice+random.randrange(-10, 10, 1)
        quantity = int(row.quantity)
        current_valuation = current_market_price*quantity
        total_bond_valuation = total_bond_valuation+current_valuation
        current_investment = row.averagePrice*quantity
        total_bond_investment = total_bond_investment+current_investment
        unrealized_PL = current_valuation-current_investment
        total_bond_unrealized_pl = total_bond_unrealized_pl+unrealized_PL
        bondName = session.query(BondDescrp.bondName).filter(BondDescrp.isin==row.isin).one()[0]
        bond_details_data.append({'name': bondName, 'quantity': quantity,'investment':current_investment, 
                                    'ticker': row.ticker ,'currentValuation':current_valuation ,'unrealizedPL': unrealized_PL })
    total_unrealized_pl = total_bond_unrealized_pl+total_stock_unrealized_pl
    total_valuation = total_stock_valuation+total_bond_valuation
    stock_valuation_percentage = (total_stock_valuation/total_valuation)*100
    stock_unrealized_pl_percentage = (total_stock_unrealized_pl/total_unrealized_pl)*100
    bond_valuation_percentage = (total_bond_valuation/total_valuation)*100
    bond_unrealized_pl_percentage = (total_bond_unrealized_pl/total_unrealized_pl)*100
    stock_summary = {'investment': total_stock_investment,'currentValuation': total_stock_valuation, 'currentValuationPercentage': stock_valuation_percentage,'unrealizedPL': total_stock_unrealized_pl, 'unrealizedPLPercentage': stock_unrealized_pl_percentage }
    bond_summary = {'investment': total_bond_investment,'currentValuation': total_bond_valuation, 'currentValuationPercentage': bond_valuation_percentage, 'unrealizedPL': total_bond_unrealized_pl, 'unrealizedPLPercentage': bond_unrealized_pl_percentage }
    for i in range(0,len(stock_details_data)):
        stock_details_data[i]['unrealizedPLPercentage'] = (stock_details_data[i]['unrealizedPL']/total_unrealized_pl)*100
        stock_details_data[i]['currentValuationPercentage'] = (stock_details_data[i]['currentValuation']/total_valuation)*100
    for i in range(0,len(bond_details_data)):
        bond_details_data[i]['unrealizedPLPercentage'] = (bond_details_data[i]['unrealizedPL']/total_unrealized_pl)*100
        bond_details_data[i]['currentValuationPercentage'] = (bond_details_data[i]['currentValuation']/total_valuation)*100
    res = [{'securityType': 'Equity', 'summaryData': stock_summary , 'detailsData' : stock_details_data},{'securityType': 'Bonds', 'summaryData': bond_summary, 'detailsData' : bond_details_data}]
    return ( res )

# NEHAL will do the changes here
def rd_arr(arr):

    for i in range( len(arr) ):
        arr[i] = round( arr[i] , 3 )

    return arr

def clienthistory():

    result = session.query( PortfolioHistory ).order_by( PortfolioHistory.date.desc() ).limit(365)
    totalInvested = []
    netPosition = []
    labels = []
    
    for res in result:
        
        totalInvested.append( res.totalInvested )
        netPosition.append( res.netPosition )
        #convert to date
        # dataname = res.date.strftime("%d %b %Y")
        labels.append( str( res.date.date() ) )

    # print(totalInvested)
    # print(netPosition)

    datasets = { "netPosition" : rd_arr(netPosition) , "totalInvested" : rd_arr(totalInvested) }
    months = [ 'Jan' , 'Feb' , 'Mar' , 'Apr' , 'May' , 'June' , 'July' , 'Aug' , 'Sep'
                , 'Oct' , 'Nov' , 'Dec' ]
    an_labels = [ 'Oct' , 'Nov' , 'Dec' , 'Jan' , 'Feb' , 'Mar'
                , 'Apr' , 'May' , 'June' , 'July' , 'Aug' , 'Sep' ]

    resp = { "datasets" : datasets, "labels" : labels , "annual_labels" : an_labels }

    return resp
