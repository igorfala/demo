from config.settings import DEBUG
import aiopg.sa   # aiohttp library for postgres
import os, sqlalchemy
from shopify.models import tables as ts1
from shopifyAuth.models import tables as ts2

# import app tables and add them here
# ex: tables += new_tabels
tables = ts1
tables += ts2

async def init_pg(app):
    """
    initiates DB connection
    """
    if DEBUG == True:
        conf = app['config']['postgres']
        engine = await aiopg.sa.create_engine(
            database=conf['database'],
            user=conf['user'],
            password=conf['password'],
            host=conf['host'],
            port=conf['port'],
            minsize=conf['minsize'],
            maxsize=conf['maxsize'],
            loop=app.loop)
    else:
        DEFAULT_DB_ENV = os.environ['DATABASE_URL']
        engine = await aiopg.sa.create_engine(DEFAULT_DB_ENV)

    app['db'] = engine

async def close_pg(app):
    """
    closes DB connection
    """
    app['db'].close()
    await app['db'].wait_closed()

# for migrating
def engine_pg(url):
    """
    @url: url of the DB
    method to create sqlalchemy engine 
    """
    if DEBUG == True:
        #conf = app['postgres']
        engine = sqlalchemy.create_engine(
            url
            )
    else:
        DEFAULT_DB_ENV = os.environ['DATABASE_URL']
        engine = sqlalchemy.create_engine(DEFAULT_DB_ENV)

    return engine
