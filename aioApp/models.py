from aioApp.settings import DEBUG
import sqlalchemy as sa
import aiopg.sa   # aiohttp library for postgres
import os

meta = sa.MetaData()

question = sa.Table(
    'question', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('question_text', sa.String(200), nullable=False),
    sa.Column('pub_date', sa.Date, nullable=False),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='question_id_pkey'))

choice = sa.Table(
    'choice', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('question_id', sa.Integer, nullable=False),
    sa.Column('choice_text', sa.String(200), nullable=False),
    sa.Column('votes', sa.Integer, server_default="0", nullable=False),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='choice_id_pkey'),
    sa.ForeignKeyConstraint(['question_id'], [question.c.id],
                            name='choice_question_id_fkey',
                            ondelete='CASCADE'),

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
