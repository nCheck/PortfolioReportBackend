import flask
import os
from flask import jsonify, request , send_from_directory
from flask import flash, redirect, url_for, session
from flask_cors import CORS, cross_origin
import requests, json
import pandas as pd
import requests


#custom

#orm models
from models.transactions import Transactions
from models.currentPortfolio import CurrentPortfolio
from models.portfolioHistory import PortfolioHistory
from models.dbconnect import getEngine

from utils import topthreecards , securitydistgraph , sectordistgraph , tabledata , clienthistory
from ltp import lastTradedPrice , getISIN
from helper_pdfgen import getPdf

#inbuilt
from sqlalchemy.orm import sessionmaker
import datetime
from random import randint

engine = getEngine()
Session = sessionmaker(bind = engine)
session = Session()

UPLOAD_FOLDER = 'uploads'

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
cors = CORS(app, resources={r"/*": {"origins": "*"}})



@app.route('/', methods=['GET','POST'])
def home():
    return "Welcome To My App"


#sample db test

@app.route('/test', methods=['GET','POST'])
def test():

    stocks = session.query(Transactions.ticker).filter(Transactions.typeOfInstrument == 'STOCK').distinct()
    res = { "Our Stocks" : list(stocks) }
    return jsonify( res )



@app.route('/api', methods=['GET','POST'])
def api():

    _topthreecards = topthreecards()
    _securitydistgraph = securitydistgraph()
    _sectordistgraph = sectordistgraph()
    _tabledata = tabledata()
    _clienthistory = clienthistory()

    resp = { "TopThreeCards" : _topthreecards , "SecurityDistGraph" : _securitydistgraph ,
             "SectorDistGraph" : _sectordistgraph , "TableData" : _tabledata, "ClientHistory": _clienthistory  }


    return jsonify( resp )



@app.route('/pdf', methods=['GET', 'POST'])
def download():
    getPdf()
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename='portfolio.pdf')

if __name__ == '__main__':
    app.run()