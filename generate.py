#custom
from models.transactions import Transactions
from models.currentPortfolio import CurrentPortfolio
from models.portfolioHistory import PortfolioHistory
from models.dbconnect import getEngine
from ltp import lastTradedPrice , getISIN , isBond

#inbuilt
from sqlalchemy.orm import sessionmaker
import datetime
from random import randint

engine = getEngine()
Session = sessionmaker(bind = engine)
session = Session()



sdate = datetime.datetime(2019, 1, 2)   # start date
edate = datetime.datetime(2020, 9, 16)   # end date

delta = edate - sdate       # as timedelta
DATES = []
for i in range(delta.days + 1):
    day = sdate + datetime.timedelta(days=i)
    DATES.append(day)




def insertCurrentPortfolio(  typeOfInstrument , isin , ticker , quantity , clientId , averagePrice ):

    cp = CurrentPortfolio( typeOfInstrument = typeOfInstrument , isin = isin , ticker = ticker
                        , quantity = quantity , clientId = clientId , averagePrice = averagePrice )

    session.add(cp)
    session.commit()





# genCurrentPortfolioFullData()

def genFullData():



    stocks = session.query(Transactions.ticker).filter().distinct()
    stocks = list(map( lambda x : x[0] , stocks ))
    
    clients = session.query(Transactions.clientId).filter().distinct()
    clients = list(map( lambda x : x[0] , clients))

    dates = DATES

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
           
                _ltp = lastTradedPrice(stock , buy_price , date)

                try : 

                    current_stock_port = session.query(CurrentPortfolio).filter( CurrentPortfolio.ticker == stock 
                                                        , CurrentPortfolio.clientId == client ).one()

                    cur_qnt = current_stock_port.quantity
                    cur_price = current_stock_port.averagePrice

                    _net_quantity =  cur_qnt + buy_qnt - sell_qnt


                    new_averagePrice = cur_price

                    if _net_quantity > cur_qnt :
                        dif = _net_quantity - cur_qnt
                        new_averagePrice = ( ( cur_price*cur_qnt ) + ( buy_price * dif ) ) / _net_quantity


                    session.query( CurrentPortfolio ).filter( CurrentPortfolio.ticker == stock
                         , CurrentPortfolio.clientId == client).update( {
                             CurrentPortfolio.quantity: _net_quantity , CurrentPortfolio.averagePrice: round( new_averagePrice , 2 )
                         } , synchronize_session = False )

                    # print("updating==========")

                except :

                    
                    _net_quantity = buy_qnt - sell_qnt
                    _realisedProfit = (buy_price*sell_qnt) - (sell_price * sell_qnt)
                    _totalInvested = ( buy_price*_net_quantity   )
                    # _netPosition = ( _ltp * _net_quantity )
                    

                    if _net_quantity != 0:

                        typeOfInstrument = 'STOCK'

                        if isBond(stock):
                            typeOfInstrument='BOND'

                        cp = CurrentPortfolio( typeOfInstrument=typeOfInstrument , ticker=stock ,
                                quantity=_net_quantity , isin=getISIN(stock) , clientId=client , averagePrice= round( buy_price , 2 )  )
                        
                        session.add(cp)


                    
            

            session.commit()

            totalInvested = 0.0
            netPosition = 0.0
            cpfs = session.query(CurrentPortfolio).filter(CurrentPortfolio.clientId==client)

            for cpf in cpfs:

                ticker = cpf.ticker
                quantity = cpf.quantity
                averagePrice = cpf.averagePrice
                _ltp = lastTradedPrice(ticker , averagePrice , date)

                totalInvested += (quantity * averagePrice)
                netPosition +=  (quantity * _ltp)


            cph = PortfolioHistory( clientId=client , totalInvested= round( totalInvested , 2 ) , netPosition= round( netPosition , 2 ) , date=date )
            
            session.add(cph)
            session.commit()

    
        


genFullData()