from config.settings import DEBUG
import sqlalchemy as sa
import aiopg.sa   # aiohttp library for postgres
import os

meta = sa.MetaData()

shop_users = sa.Table(
    'shop_users', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('first_name', sa.String(200), nullable=False),
    sa.Column('last_name', sa.String(200), nullable=False),
    sa.Column('email', sa.String(200), nullable=False),
    sa.Column('account_owner', sa.Boolean),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='shop_id_pkey'),
    )

shops = sa.Table(
    'shops', meta,
    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
    sa.Column('scope', sa.String(500) ),
    sa.Column('associated_user_scope', sa.String(200)),
    sa.Column('associated_user_id', sa.Integer, ),
    sa.Column('timestamp', sa.Integer, ),
    sa.Column('access_token', sa.String(200),  ),
    sa.Column('state', sa.String(200), ),
    sa.Column('code', sa.String(200), ),
    sa.Column('shop', sa.String(200), unique=True),
    sa.Column('hmac', sa.String(200), ),
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
