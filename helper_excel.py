
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




writer = pd.ExcelWriter('uploads/portfolio.xlsx', engine='xlsxwriter')
client_id='J001'

broker_name='AIM'

def createExcel(sheetname,cid,sheet_st,broker,df):
   
    
    
    df.to_excel(writer, sheet_name=sheetname,startrow=10,startcol=1)
    worksheet = writer.sheets[sheetname]
    worksheet.set_column('B:M',18)
    cell_format = writer.book.add_format({'bold': True, 'italic': True,'color':'blue'})
    worksheet.write('B2',broker,cell_format)
    worksheet.write('B5','Client ID')
    worksheet.write('C5',cid)
    worksheet.write('B7',sheet_st)
  
#summary method


def summary(security,holdings,currentval,unrealized,unrealizedper):

    sec_type=security
    holdings_buy_value=holdings
    current_value=currentval
    unrealized_pl=unrealized
    unrealized_pl_percent=unrealizedper
    
    sheetname='SUMMARY'
    summary_st='SUMMARY Statement as on '+str(datetime.date.today())
    summary = {'Security Type': sec_type,
            'Holdings Buy Value': holdings_buy_value,'Current Value':current_value,'Unrealized P&L':unrealized_pl,'Unrealized P&L%':unrealized_pl_percent
            }
    df1 = pd.DataFrame(summary, columns = ['Security Type', 'Holdings Buy Value','Current Value','Unrealized P&L','Unrealized P&L%'])
    df1.set_index('Security Type', inplace=True)

    createExcel(sheetname,client_id,summary_st,broker_name,df1)

    
def equity(symbol,isin,sector,quant,buy,holdings,prevprice,currentval,unrealized,unrealizedper):

    Symbol=symbol
    ISIN=isin
    SECTOR=sector
    qty=quant
    buy_av=buy
    holdings_buy_value=holdings
    prev_clos_price=prevprice
    current_value=currentval
    unrealized_pl=unrealized
    unrealized_pl_percent=unrealizedper
    
    sheetname='EQ HOLDINGS'
    summary_st='Eq Holdings Statement as on '+str(datetime.date.today())
    eqholding={'Symbol':Symbol,'ISIN':ISIN,'SECTOR':SECTOR,'Qty Available':qty,'Buy Average':buy_av,'Holdings Buy Value':holdings_buy_value,'Previous Closing Price':prev_clos_price,'Current Value':current_value,'Unrealized P&L':unrealized_pl,'Unrealized P&L%':unrealized_pl_percent}
    df2 = pd.DataFrame(eqholding, columns = ['Symbol', 'ISIN','SECTOR','Qty Available','Buy Average','Holdings Buy Value','Previous Closing Price','Current Value','Unrealized P&L','Unrealized P&L%'])
    df2.set_index('Symbol', inplace=True)

    createExcel(sheetname,client_id,summary_st,broker_name,df2)
    
    
def bonds(symbol,isin,sector,quant,buy,holdings,prevprice,currentval,unrealized,unrealizedper,accrued,maturity):

    Symbol=symbol
    ISIN=isin
    SECTOR=sector
    qty=quant
    buy_av=buy
    holdings_buy_value=holdings
    prev_clos_price=prevprice
    current_value=currentval
    unrealized_pl=unrealized
    unrealized_pl_percent=unrealizedper
    accrued_int=accrued
    mat_date=maturity

    sheetname='BOND HOLDINGS'
    summary_st='BOND Holdings Statement as on '+str(datetime.date.today())
    bondholding={'Symbol':Symbol,'ISIN':ISIN,'SECTOR':SECTOR,'Qty Available':qty,'Buy Average':buy_av,'Holdings Buy Value':holdings_buy_value,'Previous Closing Price':prev_clos_price,'Current Value':current_value,'Unrealized P&L':unrealized_pl,'Unrealized P&L%':unrealized_pl_percent,'Accrued Interest':accrued_int,'Maturity Date':mat_date}
    df3 = pd.DataFrame(bondholding, columns = ['Symbol', 'ISIN','SECTOR','Qty Available','Buy Average','Holdings Buy Value','Previous Closing Price','Current Value','Unrealized P&L','Unrealized P&L%','Accrued Interest','Maturity Date'])
    df3.set_index('Symbol', inplace=True)

    createExcel(sheetname,client_id,summary_st,broker_name,df3)

def saveExcel():
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

def invAndVal():

    card1 = topthreecards()['card1']
    total_investment = card1['value1']
    total_valuation = card1['value2']
    resp = {
        'Investment' : total_investment , 'Valuation' : total_valuation
    }
    return resp


def rd(num):
    return round( num , 3)

def genexel():

    tableData = tabledata()
    sec_disti = securitydistgraph()
    stockData = tableData[0]
    bondData = tableData[1]

    stock_summary = stockData['summaryData']
    stock_details = stockData['detailsData']
    bond_summary = bondData['summaryData']
    bond_details = bondData['detailsData']


    
    eSymbol , eISIN , eSECTOR , eqty , ebuy_av , eholdings_buy_value , eprev_clos_price , ecurrent_value , eunrealized_pl , eunrealized_pl_percent = [] , [] , [] , [] , [] , [] , [] , [] , [] , []

    for stock in stock_details:

        ticker = stock['ticker']
        eSymbol.append(ticker)

        isin = getISIN(ticker)
        eISIN.append(isin)

        name = stock['name']
        
        sector = getStockSector(ticker)
        eSECTOR.append(sector)

        qty = rd( stock['quantity'] )
        eqty.append( qty )

        buy_average = rd( stock['currentValuation'] / qty )
        ebuy_av.append( buy_average )

        prevClosePrice = rd( lastTradedPrice(ticker) )
        eprev_clos_price.append( prevClosePrice )


        hldin_buy_val = rd( stock['investment'] )
        eholdings_buy_value.append( hldin_buy_val )

        curr_val = rd( stock['currentValuation'] )
        ecurrent_value.append( curr_val )

        unrealizedPL = rd( stock['unrealizedPL'] )
        eunrealized_pl.append( unrealizedPL )

        unrealizedPLPercentage = rd( stock['unrealizedPLPercentage'] )
        eunrealized_pl_percent.append( unrealizedPLPercentage )



    bsymbol, bisin, bsector, bquant, bbuy, bholdings, bprevprice, bcurrentval, bunrealized, bunrealizedper, baccrued, bmaturity = [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , []
    
    for bond in bond_details:

        ticker = bond['ticker']
        bsymbol.append( ticker )
        
        isin = getISIN(ticker)
        bisin.append( isin )

        name = bond['name']
        
        sector = getStockSector(ticker)
        bsector.append( sector )

        qty = rd( bond['quantity'] )
        bquant.append( qty )

        buy_average = rd( bond['currentValuation'] / qty )
        bbuy.append( buy_average )

        #stub
        prevClosePrice = rd( lastTradedPrice(ticker , buy_average) )
        bprevprice.append( prevClosePrice )


        hldin_buy_val = rd( bond['investment'] )
        bholdings.append( hldin_buy_val )

        curr_val = rd( bond['currentValuation'] )
        bcurrentval.append( curr_val )

        unrealizedPL = rd( bond['unrealizedPL'] )
        bunrealized.append( unrealizedPL )

        unrealizedPLPercentage = rd( bond['unrealizedPLPercentage'] )
        bunrealizedper.append( unrealizedPLPercentage )

        spc1 = 12
        baccrued.append( spc1 )

        spc2 = 15
        bmaturity.append( spc2 )


    
    
    eq_inv = rd( stock_summary['investment'] )
    eq_val = rd( stock_summary['currentValuation'] )
    eunrlpl = rd( stock_summary['unrealizedPL'] )
    eunrlper = rd( stock_summary['unrealizedPLPercentage'] )
    epfperc = rd( sec_disti['datasets'][0] )


    bd_inv = rd( bond_summary['investment'] )
    bd_val = rd( bond_summary['currentValuation'] )
    bunrlpl = rd( bond_summary['unrealizedPL'] )
    bunrlper = rd( bond_summary['unrealizedPLPercentage'] )
    bpfperc = rd( sec_disti['datasets'][1] )

    security = ['Equity','Bond','TOTAL']
    holdings = [ eq_inv , bd_inv , eq_inv + bd_inv ]
    currentval = [ eq_val , bd_val , eq_val + bd_val ]
    unrealized = [ eunrlpl , bunrlpl , eunrlpl + bunrlpl ]
    unrealizedper = [ eunrlper , bunrlper , 100 ]


    summary(security,holdings,currentval,unrealized,unrealizedper)
    equity( eSymbol , eISIN , eSECTOR , eqty , ebuy_av , eholdings_buy_value , eprev_clos_price , ecurrent_value , eunrealized_pl , eunrealized_pl_percent )
    bonds(bsymbol, bisin, bsector, bquant, bbuy, bholdings, bprevprice, bcurrentval, bunrealized, bunrealizedper, baccrued, bmaturity)
    ss = [ bsymbol, bisin, bsector, bquant, bbuy, bholdings, bprevprice, bcurrentval, bunrealized, bunrealizedper, baccrued, bmaturity ]
    for s in ss:
        print( len(s) , "->" , s )
    saveExcel()






# genexel()

