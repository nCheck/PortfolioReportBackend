#custom
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

#insert one data
def test():

    cp = PortfolioHistory( clientId = 'J001' , totalInvested = 785.1
            , netPosition = 800.5 , date = datetime.datetime.now() )

    session.add(cp)
    session.commit()


def gr():
    return randint(1,122254)



TICKERS = ['AAPL','TSLA','AMZN','CSCO','SYRS']

#insert bulk data
def insertTransaction():

    trans = []

    for i in range(1,10):

        for j in range(3):
            t = Transactions( clientId = 'J001' , typeOfInstrument = 'STOCK' , action = 'SELL'
                        , isin='5001' , ticker= TICKERS[ gr()%5 ] , quantity=( 2 ) , price=( 200 - gr()%30 )
                        , timestamp= datetime.datetime(2020,9,i) , brokerCode = 'NASDAQ' )
            
            trans.append(t)

    session.add_all(trans)

    session.commit()


# insertTransaction()


def getTransactions():

    res = session.query(Transactions).filter(Transactions.timestamp == datetime.datetime(2020,9,1) )

    for r in res:
        print(r)


def insertCurrentPortfolio(  typeOfInstrument , isin , ticker , quantity , clientId , averagePrice ):

    cp = CurrentPortfolio( typeOfInstrument = typeOfInstrument , isin = isin , ticker = ticker
                        , quantity = quantity , clientId = clientId , averagePrice = averagePrice )

    session.add(cp)
    session.commit()



def genCurrentPortfolioFullData():

    # only stocks for now
    # results = session.query(Transactions).filter(Transactions.typeOfInstrument == 'STOCK')
    stocks = session.query(Transactions.ticker).filter(Transactions.typeOfInstrument == 'STOCK').distinct()
    
    stocks = list(map( lambda x : x[0] , stocks ))
    

    clients = session.query(Transactions.clientId).filter(Transactions.typeOfInstrument == 'STOCK').distinct()
    clients = list(map( lambda x : x[0] , clients))

    for client in clients:

        stockmap_b = { stock : { 'averagePrice' : 0.0 , 'quantity' : 0.0 } for stock in stocks }
        stockmap_s = { stock : { 'averagePrice' : 0.0 , 'quantity' : 0.0 } for stock in stocks }



        # get all buy stocks of client
        clientres = session.query(Transactions).filter(Transactions.typeOfInstrument == 'STOCK' ,
                                            Transactions.clientId == client)

            
        for result in clientres:

            price = result.price
            quantity = result.quantity
            stock = result.ticker

            if result.action == 'BUY':

                old_quantity = stockmap_b[stock]['quantity']
                old_price = stockmap_b[stock]['averagePrice']
                new_quantity = old_quantity + quantity
                new_price = ( ( old_quantity*old_price ) + (quantity * price) ) / ( new_quantity )

                stockmap_b[stock]['quantity'] = new_quantity
                stockmap_b[stock]['averagePrice'] = new_price

            else:

                old_quantity = stockmap_s[stock]['quantity']
                old_price = stockmap_s[stock]['averagePrice']
                new_quantity = old_quantity + quantity
                new_price = ( ( old_quantity*old_price ) + (quantity * price) ) / ( new_quantity )

                stockmap_s[stock]['quantity'] = new_quantity
                stockmap_s[stock]['averagePrice'] = new_price

        


        
        print(stockmap_b)
        print(stockmap_s)


# genCurrentPortfolioFullData()

def genFullData():

    # only stocks for now
    # results = session.query(Transactions).filter(Transactions.typeOfInstrument == 'STOCK')

    stocks = session.query(Transactions.ticker).filter(Transactions.typeOfInstrument == 'STOCK').distinct()
    stocks = list(map( lambda x : x[0] , stocks ))
    
    clients = session.query(Transactions.clientId).filter(Transactions.typeOfInstrument == 'STOCK').distinct()
    clients = list(map( lambda x : x[0] , clients))

    dates = session.query(Transactions.timestamp).filter(Transactions.typeOfInstrument == 'STOCK').distinct()

    # for i in range(1,10):
    #     dates.append( datetime.datetime(2020,9,i) )


    for date in dates:

        results = session.query(Transactions).filter(Transactions.timestamp == date)

        for client in clients:

            stockmap_b = { stock : { 'averagePrice' : 0.0 , 'quantity' : 0.0 } for stock in stocks }
            stockmap_s = { stock : { 'averagePrice' : 0.0 , 'quantity' : 0.0 } for stock in stocks }

            vis_stock = set()
                
            for result in results:

                price = result.price
                quantity = result.quantity
                stock = result.ticker
                

                if result.action == 'BUY' and result.clientId == client :

                    old_quantity = stockmap_b[stock]['quantity']
                    old_price = stockmap_b[stock]['averagePrice']
                    new_quantity = old_quantity + quantity
                    new_price = ( ( old_quantity*old_price ) + (quantity * price) ) / ( new_quantity )

                    stockmap_b[stock]['quantity'] = new_quantity
                    stockmap_b[stock]['averagePrice'] = new_price

                    vis_stock.add(stock)

                elif result.clientId == client :

                    old_quantity = stockmap_s[stock]['quantity']
                    old_price = stockmap_s[stock]['averagePrice']
                    new_quantity = old_quantity + quantity
                    new_price = ( ( old_quantity*old_price ) + (quantity * price) ) / ( new_quantity )

                    stockmap_s[stock]['quantity'] = new_quantity
                    stockmap_s[stock]['averagePrice'] = new_price

                    vis_stock.add(stock)


            realisedProfit = 0.0

            for stock in vis_stock:

                buy_price = stockmap_b[stock]['averagePrice']
                buy_qnt = stockmap_b[stock]['quantity']
                sell_price = stockmap_s[stock]['averagePrice']
                sell_qnt = stockmap_s[stock]['quantity']
                _ltp = lastTradedPrice(stock , buy_price)

                try : 
                    current_stock_port = session.query(CurrentPortfolio).filter( CurrentPortfolio.ticker == stock 
                                                        , CurrentPortfolio.clientId == client ).one()

                    cur_qnt = current_stock_port.quantity
                    cur_price = current_stock_port.averagePrice

                    _net_quantity =  cur_qnt + buy_qnt - sell_qnt
                    _realisedProfit =  ( cur_qnt*cur_price ) + (buy_price*sell_qnt) - (sell_price * sell_qnt)

                    new_averagePrice = cur_price

                    if _net_quantity > cur_qnt :
                        dif = _net_quantity - cur_qnt
                        new_averagePrice = ( ( cur_price*cur_qnt ) + ( buy_price * dif ) ) / dif

                    _netPosition = _ltp * _net_quantity

                    session.query( CurrentPortfolio ).filter( CurrentPortfolio.ticker == stock
                         , CurrentPortfolio.clientId == client).update( {
                             CurrentPortfolio.quantity: _net_quantity , CurrentPortfolio.averagePrice: new_averagePrice
                         } , synchronize_session = False )

                    # print("updating==========")

                except :

                    
                    _net_quantity = buy_qnt - sell_qnt
                    _realisedProfit = (buy_price*sell_qnt) - (sell_price * sell_qnt)
                    _totalInvested = ( buy_price*_net_quantity   )
                    _netPosition = ( _ltp * _net_quantity )
                    
                    print(_net_quantity , stock ,_totalInvested , _netPosition )

                    if _net_quantity != 0:

                        cp = CurrentPortfolio( typeOfInstrument='STOCK' , ticker=stock ,
                                quantity=_net_quantity , clientId=client , averagePrice=buy_price )
                        
                        session.add(cp)


                    
            

            session.commit()

            totalInvested = 0.0
            netPosition = 0.0
            cpfs = session.query(CurrentPortfolio).filter(CurrentPortfolio.clientId==client)

            for cpf in cpfs:

                ticker = cpf.ticker
                quantity = cpf.quantity
                averagePrice = cpf.averagePrice
                _ltp = lastTradedPrice(ticker , averagePrice)

                totalInvested += quantity * averagePrice
                netPosition +=  quantity * _ltp


            cph = PortfolioHistory( clientId=client , totalInvested=totalInvested , netPosition=netPosition , date=date )
            
            session.add(cph)
            session.commit()

    
        

                


            








# checkExist()
genFullData()
