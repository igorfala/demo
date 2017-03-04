from config.settings import DEBUG
import aiopg.sa   # aiohttp library for postgres
import os

async def init_pg(app):
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
    app['db'].close()
    await app['db'].wait_closed()
