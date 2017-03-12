from config.settings import DEBUG, APP_CONF
from sqlalchemy_utils import EncryptedType
import sqlalchemy as sa
import aiopg.sa   # aiohttp library for postgres
import os

encrypion_key = APP_CONF['postgres']['encrypion_key']
meta = sa.MetaData()

question = sa.Table(
    'question', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('question_text', EncryptedType(sa.String(200), encrypion_key ), nullable=False),
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
                            )
# Please add all the tables to this list
tables = [
        question,
        choice
        ]
