from sqlalchemy import create_engine

def getEngine():

    url = 'housestack.crzf2jqpqelj.us-east-2.rds.amazonaws.com'
    username = 'admin'
    password = 'housestack'
    db = 'PROD'
    dbpath = f'mysql://{username}:{password}@{url}/{db}'

    # engine = create_engine( dbpath , echo = True)
    engine = create_engine( dbpath , echo = False)

    return engine


