
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

from ltp import lastTradedPrice , getISIN , getStockSector
from utils import topthreecards , securitydistgraph , sectordistgraph , tabledata , clienthistory
from pdfgen import generatePDF

#inbuilt
from sqlalchemy.orm import sessionmaker
import datetime
from random import randint

engine = getEngine()
Session = sessionmaker(bind = engine)
session = Session()

    



def rd(num):
    return round( num , 3)

def helperPdfgen():

    tableData = tabledata()
    sec_disti = securitydistgraph()
    stockData = tableData[0]
    bondData = tableData[1]

    stock_summary = stockData['summaryData']
    stock_details = stockData['detailsData']
    bond_summary = bondData['summaryData']
    bond_details = bondData['detailsData']

    equityTrades = []

    for stock in stock_details:

        ticker = stock['ticker']
        name = stock['name']
        
        sector = getStockSector(ticker)
        qty = rd( stock['quantity'] )
        buy_average = rd( stock['currentValuation'] / qty )
        #stub
        prevClosePrice = rd( lastTradedPrice(ticker) )
        hldin_buy_val = rd( stock['investment'] )
        curr_val = rd( stock['currentValuation'] )
        unrealizedPL = rd( stock['unrealizedPL'] )
        unrealizedPLPercentage = rd( stock['unrealizedPLPercentage'] )
        spc1 = ''
        spc2 = ''
        
        p_portf = '10%'

        tm = [name , sector , qty , buy_average , prevClosePrice,
                hldin_buy_val , curr_val , unrealizedPL , unrealizedPLPercentage ,
                spc1 , spc2 , p_portf]

        equityTrades.append( tm )



    bondTrades = []
    
    for bond in bond_details:

        ticker = bond['ticker']
        name = bond['name']
        
        sector = getStockSector(ticker)
        qty = rd( bond['quantity'] )
        buy_average = rd( bond['currentValuation'] / qty )
        #stub
        prevClosePrice = rd( lastTradedPrice(ticker , buy_average) )
        hldin_buy_val = rd( bond['investment'] )
        curr_val = rd( bond['currentValuation'] )
        unrealizedPL = rd( bond['unrealizedPL'] )
        unrealizedPLPercentage = rd( bond['unrealizedPLPercentage'] )
        spc1 = ''
        spc2 = ''
        
        p_portf = '10%'

        tm = [name , sector , qty , buy_average , prevClosePrice,
                hldin_buy_val , curr_val , unrealizedPL , unrealizedPLPercentage ,
                spc1 , spc2 , p_portf]

        bondTrades.append( tm )


    
    eq_inv = rd( stock_summary['investment'] )
    eq_val = rd( stock_summary['currentValuation'] )
    unrlpl = rd( stock_summary['unrealizedPL'] )
    unrlper = rd( stock_summary['unrealizedPLPercentage'] )
    
    pfperc = rd( sec_disti['datasets'][0] )

    Equity = [ eq_inv , eq_val , unrlpl , unrlper , pfperc ]

    bd_inv = rd( bond_summary['investment'] )
    bd_val = rd( bond_summary['currentValuation'] )
    unrlpl = rd( bond_summary['unrealizedPL'] )
    unrlper = rd( bond_summary['unrealizedPLPercentage'] )
    
    pfperc = rd( sec_disti['datasets'][1] )

    FI = [ bd_inv , bd_val , unrlpl , unrlper , pfperc ]


    resp = {
        "FI":FI , "Equity" : Equity , "equityTrades" : equityTrades,
        "bondTrades" : bondTrades
    }

    print(FI)
    print(Equity)
    print(bondTrades)

    return resp



def historyHelper():

    cli_hist = clienthistory()
    datasets = cli_hist['datasets']
    netPosition = datasets['netPosition']
    totalInvested = datasets['totalInvested']

    monthlyInv = []
    monthlyVal = []

    for i in range( 0 , len( netPosition ) , 25 ):
        monthlyInv.append( totalInvested[i] )
        monthlyVal.append( netPosition[i] )
    

    monthlyInv = monthlyInv[:12]
    monthlyVal = monthlyVal[:12]


    print("len", len(monthlyVal))

    labels = cli_hist['annual_labels']

    resp = {
        "monthlyVal": monthlyVal[::-1], "monthlyInv": monthlyInv[::-1], "labels" : labels
    }

    return resp


def invAndVal():

    card1 = topthreecards()['card1']
    total_investment = card1['value1']
    total_valuation = card1['value2']
    resp = {
        'Investment' : total_investment , 'Valuation' : total_valuation
    }
    return resp



def getPdf():

    resp = helperPdfgen()
    histdata = historyHelper()

    FI= resp['FI']
    Equity= resp['Equity']

    iv = invAndVal()
    Investment = iv['Investment']
    Valuation = iv['Valuation']
    monthlyInv = histdata['monthlyInv']
    monthlyVal = histdata['monthlyVal']
    labels = histdata['labels']

    equityTrades = resp['equityTrades']

    bondTrades= resp['bondTrades']

    URPL = rd(Valuation - Investment )
    perURPL = rd( URPL*100 / ( Valuation ) )
    #Page 5 data
    net_position=[
            ['Total Portfolio','','','','','', rd(Investment) , rd(Valuation) , URPL , perURPL ,'100%','100%']
        ]

    generatePDF(FI,Equity,Investment,Valuation,monthlyInv,monthlyVal,equityTrades,bondTrades,net_position,labels)




# getPdf()