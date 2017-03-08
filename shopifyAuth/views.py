from aiohttp import web, ClientSession
from config.settings import CONFIG_DIR, APP_CONF, SHOPS_DIR
from shopifyAuth.helpers.shopify import SHOPIFY_AUTH_URI, process_token_data
from shopifyAuth.models import shops, shop_users
import aiohttp_jinja2
import yaml
import uuid
import os
import json
import sqlalchemy

# first page form
@aiohttp_jinja2.template('auth.html')
async def auth(request):
    if request.method == 'POST':
        data = await request.post()
        shop = data['shop']
        host = request.url
        url = str(host) + 'connect_shopify/' + shop
        return web.Response(
            status=302,
            headers={
                'location': url,
            },
        )

    else:
        return

# redirects to shopify auth with shop name
async def connect_shopify(request):
    async with request.app['db'].acquire() as conn:
        shop = request.match_info['shop']
        nonce = uuid.uuid4().hex
        SHOPIFY_AUTH_URL = SHOPIFY_AUTH_URI.format(shop, nonce)
        #CONFIG_FILE = os.path.join(SHOPS_DIR, shop)

        #with open(CONFIG_FILE, "w") as yaml_file:
        #    yaml_file.write(yaml.dump({"state": nonce}, default_flow_style=False))
        cursor = await conn.execute(shops.select().where(shops.c.shop == shop))
        # update if exists or create
        if not await cursor.fetchone():
            print(' shop created')
            cursor = await conn.execute(shops.insert().values(state=nonce, shop=shop))
        else:
            print('shop updated')
            cursor = await conn.execute(shops.update().where(shops.c.shop==shop).values(state=nonce))

        return web.Response(
            status=302,
            headers={
                'location': SHOPIFY_AUTH_URL,
            },
        )

# callback from shopify
async def callback_shopify(request):
    async with request.app['db'].acquire() as conn:

        data = dict(request.rel_url.query)
        #validate the shop params
        nonce = data['state']
        shop = data['shop']
        code = data['code']

        # checking that it's coming from shopify
        if '.myshopify.com' in shop:
            shop = shop.replace('.myshopify.com', '')
            try:
                cursor = await conn.execute(shops.select().where(shops.c.shop == shop))
                row = await cursor.fetchone()
                state = row.state

            except Exception as e:
                print('Reason: {}'.format(e))
                return web.Response(text='NOT AUTHORIZED')

            if state == nonce:

                token_data = await get_token(shop, code)
                token_data['shop'] = shop
                data.update(token_data)
                shop_data, shop_user_data = process_token_data(data)
                if shop_user_data:
                    cursor = await conn.execute(shop_users.select().where(shop_users.c.id==shop_user_data['id']))
                    # update if exists or create
                    if not await cursor.fetchone():
                        print(' shop user created')
                        cursor = await conn.execute(shop_users.insert().values(**shop_user_data))
                    else:
                        print('shop user updated')
                        cursor = await conn.execute(shop_users.update().where(shop_users.c.id==shop_user_data['id']).values(**shop_user_data))
                await conn.execute(shops.update().where(shops.c.shop==shop).values(**shop_data))

                SHOP_URL = 'https://{}.myshopify.com'.format(shop)
                return web.Response(
                status=302,
                headers={
                    'location': SHOP_URL,
                    },
                    )

            print('INCORECT NONCE')
        print('REQUEST NOT FROM SHOPIFY')
    return web.Response(text='NOT AUTHORIZED')

# gets the token data
async def get_token(shop, code):
    async with ClientSession() as session:
        url = APP_CONF['shopify']['admin_uri'].format(shop)
        headers = {"Content-type": "application/json",}
        payload = {}
        payload['client_id'] = APP_CONF['shopify']['key']
        payload['client_secret'] = APP_CONF['shopify']['secret']
        payload['code'] = code

        async with session.post(url, data=json.dumps(payload),\
                                     headers=headers) as resp:
            return await resp.json()
