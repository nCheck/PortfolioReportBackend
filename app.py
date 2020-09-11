import flask
import os
from flask import jsonify, request
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

@app.route('/test', methods=['GET','POST'])
def test():

    stocks = session.query(Transactions.ticker).filter(Transactions.typeOfInstrument == 'STOCK').distinct()
    res = { "Our Stocks" : list(stocks) }
    return jsonify( res )





app.run(port=3000)