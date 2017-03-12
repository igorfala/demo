from config.settings import DEBUG, APP_CONF
from sqlalchemy_utils import EncryptedType
import sqlalchemy as sa
import aiopg.sa   # aiohttp library for postgres
import os

encrypion_key = APP_CONF['postgres']['encrypion_key']
meta = sa.MetaData()
#stores data of shop user that gives authorization
shop_users = sa.Table(
    'shop_users', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('first_name', EncryptedType(sa.String(200), encrypion_key), nullable=False),
    sa.Column('last_name', EncryptedType(sa.String(200), encrypion_key), nullable=False),
    sa.Column('email', EncryptedType(sa.String(200), encrypion_key), nullable=False),
    sa.Column('account_owner', sa.Boolean),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='shop_id_pkey'),
    )
# stores all the shop token data
shops = sa.Table(
    'shops', meta,
    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
    sa.Column('scope', sa.String(500) ),
    sa.Column('associated_user_scope', sa.String(200)),
    sa.Column('associated_user_id', sa.Integer, ),
    sa.Column('timestamp', sa.Integer, ),
    sa.Column('access_token', EncryptedType(sa.String(200), encrypion_key),  ),
    sa.Column('state', EncryptedType(sa.String(200), encrypion_key), ),
    sa.Column('code', EncryptedType(sa.String(200), encrypion_key), ),
    sa.Column('shop', EncryptedType(sa.String(200), encrypion_key), unique=True),
    sa.Column('hmac', EncryptedType(sa.String(200), encrypion_key), ),
    sa.Column('expires_in', sa.Integer, ),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='shop_pkey'),
    sa.ForeignKeyConstraint(['associated_user_id'], [shop_users.c.id],\
                            name='user_associated_user_id_fkey',
                            ondelete='CASCADE'),
                            )

# Please add all the tables to this list
tables = [
        shops,
        shop_users,
        ]
