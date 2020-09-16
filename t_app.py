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


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'super secret key'
cors = CORS(app, resources={r"/*": {"origins": "*"}})



@app.route('/', methods=['GET','POST'])
def home():
    return "Welcome To My App"


#sample db test

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
    for row in stocks:
        current_market_price = (getPrice(str(row.ticker)))
        quantity = int(row.quantity)
        total_stock_valuation = total_stock_valuation+(current_market_price*quantity)
        total_investment = total_investment+(row.averagePrice*quantity)
    bonds = session.query(CurrentPortfolio).filter(CurrentPortfolio.typeOfInstrument == 'BOND')
    total_bond_valuation = 0
    for row in bonds:
        current_market_price = row.averagePrice+random.randrange(-10, 10, 1)
        quantity = int(row.quantity)
        total_bond_valuation = total_bond_valuation+current_market_price*quantity
        total_investment = total_investment+(row.averagePrice*quantity)
    total_valuation = total_stock_valuation+total_bond_valuation
    res = {'field1': "My investment",'value1': total_investment, 'field2' :"My networth",'value2':total_valuation}
    return jsonify(res)

#@app.route('/test', methods=['GET','POST'])
#def test():

#    stocks = session.query(Transactions.ticker).filter(Transactions.typeOfInstrument == 'STOCK').distinct()
#    res = { "Our Stocks" : list(stocks) }
 #   return jsonify( res )
#Practice db query
#@app.route('/securitydistgraph', methods=['GET','POST'])
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
    return jsonify( res )

def sectordistgraph():
    sector_summary = {}
    stock_details = session.query(StockDescrp)
    bond_details = session.query(BondDescrp)
    total_value = 0
    sector_labels = []
    sector_percentage = []
    for row in stock_details:
        quantity = int(session.query(CurrentPortfolio.quantity).filter(CurrentPortfolio.isin==row.isin))
        if row.sector in sector_summary.keys():
            stock_valuation = getPrice(str(row.ticker))*quantity
            updated_value = sector_summary[row.sector]+stock_valuation
            sector_summary[row.sector] = updated_value
        else:
            stock_valuation = getPrice(str(row.ticker))*quantity
            sector_summary[row.sector] = stock_valuation
        total_value = total_value+stock_valuation
    for row in bond_details:
        quantity = int(session.query(CurrentPortfolio.quantity).filter(CurrentPortfolio.isin==row.isin))
        if row.sector in sector_summary.keys():
            bond_valuation = row.parValue+random.randrange(-10, 10, 1)*quantity
            updated_value = sector_summary[row.sector]+bond_valuation
            sector_summary[row.sector] = updated_value
        else:
            bond_valuation = row.parValue+random.randrange(-10, 10, 1)*quantity
            sector_summary[row.sector] = bond_valuation
        total_value = total_value+bond_valuation
    for key in sector_summary.keys():
        sector_labels.append(key)
        sector_percentage.append((sector_summary[key]/total_value)*100)
    res = { 'labels':sector_labels,'datasets':[{'data': sector_percentage}]}
    return jsonify( res )

def tabledata():
    stocks = session.query(CurrentPortfolio).filter(CurrentPortfolio.typeOfInstrument == 'STOCK')
    total_stock_valuation = 0
    total_stock_investment = 0
    stock_details_data = []
    for row in stocks:
        current_market_price = (getPrice(str(row.ticker)))
        quantity = int(row.quantity)
        current_valuation = current_market_price*quantity
        total_stock_valuation = total_stock_valuation+current_valuation
        current_investment = row.averagePrice*quantity
        total_stock_investment = total_stock_investment+current_investment
        unrealized_PL = current_valuation-current_investment
        stockName = session.query(StockDescrp.stockName).filter(StockDescrp.isin==row.isin).one()[0]
        stock_details_data.append({'name': stockName, 'quantity': quantity, 'investment': current_investment,'currentValuation': current_valuation, 'unrealizedPL': unrealized_PL })
    stock_summary = {'investment': total_stock_investment,'currentValuation': total_stock_valuation, 'unrealizedPL': total_stock_valuation-total_stock_investment }
    bonds = session.query(CurrentPortfolio).filter(CurrentPortfolio.typeOfInstrument == 'BOND')
    total_bond_valuation = 0
    total_bond_investment = 0
    bond_details_data = []
    for row in bonds:
        current_market_price = row.averagePrice+random.randrange(-10, 10, 1)
        quantity = int(row.quantity)
        current_valuation = current_market_price*quantity
        total_bond_valuation = total_bond_valuation+current_valuation
        current_investment = row.averagePrice*quantity
        total_bond_investment = total_bond_investment+current_investment
        unrealized_PL = current_valuation-current_investment
        bondName = session.query(BondDescrp.bondName).filter(BondDescrp.isin==row.isin).one()[0]
        bond_details_data.append({'name': bondName, 'quantity': quantity,'investment':current_investment, 'currentValuation':current_valuation ,'unrealizedPL': unrealized_PL })
    bond_summary = {'investment': total_bond_investment,'currentValuation': total_bond_valuation, 'unrealizedPL': total_bond_valuation-total_bond_investment }
    res = [{'securityType': 'Equity', 'summaryData': stock_summary , 'detailsData' : stock_details_data},{'securityType': 'Bonds', 'summaryData': bond_summary, 'DetailsData' : bond_details_data}]
    return jsonify( res )


if __name__ == '__main__':
    app.run()