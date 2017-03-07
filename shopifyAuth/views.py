from aiohttp import web, ClientSession
from config.settings import CONFIG_DIR, APP_CONF, SHOPS_DIR
from shopifyAuth.helpers.shopify import SHOPIFY_AUTH_URI
from shopifyAuth.models import shops, shop_users
import aiohttp_jinja2
import yaml
import uuid
import os
import json

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
        CONFIG_FILE = os.path.join(SHOPS_DIR, shop)

        with open(CONFIG_FILE, "w") as yaml_file:
            yaml_file.write(yaml.dump({"state": nonce}, default_flow_style=False))

        cursor = await conn.execute(shops.insert().values(state=nonce, shop=shop))
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
            shop = shop.split('.myshopify.com')[0]

            CONFIG_FILE = os.path.join(SHOPS_DIR, shop)
            with open(CONFIG_FILE) as f:
                SHOP_CONF = yaml.safe_load(f)
            # retrieving state and checking for shop name
            try:
                state = await conn.execute(shops.select([state]).where(shop == shop))
            except:
                print('The shop {} is not in the database')
                return web.Response(text='NOT AUTHORIZED')

            if state == nonce:
                async with ClientSession() as session:
                    url = APP_CONF['shopify']['admin_uri'].format(shop)
                    headers = {"Content-type": "application/json",}
                    payload = {}
                    payload['client_id'] = APP_CONF['shopify']['key']
                    payload['client_secret'] = APP_CONF['shopify']['secret']
                    payload['code'] = code

                    async with session.post(url,\
                       data=json.dumps(payload),\
                       headers=headers) as resp:
                       token_data = await resp.json()
                       #token_data = json.loads(token_data)
                       print(resp.status, token_data, type(token_data), token_data, type(token_data))
                       token_data['shop'] = shop
                       data.update(token_data)

                       with open(CONFIG_FILE, "w") as yaml_file:
                           yaml_file.write(yaml.dump(data, default_flow_style=False))
                       shop_data, shop_user_data = process_token_data(data)
                       if shop_user_data:
                           await conn.execute(shop_users.insert().values(**shop_user_data))
                       await conn.execute(shops.insert().values(**shop_data))

                    with open(CONFIG_FILE) as f:
                        SHOP_CONF = yaml.safe_load(f)
                return web.Response(text=str(SHOP_CONF))
            print('INCORECT NONCE')
    return web.Response(text='NOT AUTHORIZED')

###########################
# testing
async def post_it(request):
    async with ClientSession() as session:
        host = request.host
        http = str(request.url).split(host)[0]
        url = http+host+'/post_to'
        headers = {"Content-type": "application/json",}
        payload = {}
        payload['client_id'] = APP_CONF['shopify']['key']
        payload['client_secret'] = APP_CONF['shopify']['secret']
        payload['code'] = '468b0ab605c66c2e597aa8859c2af0f7'
        print(headers)
        async with session.post(url,\
           data=json.dumps(payload),\
           headers=headers) as resp:
           print(resp.status)
           print(await resp.text())
    return web.Response(text=await resp.text())

async def post_to(request):
    data = await request.json()
    print(request.headers)
    CONFIG_FILE = os.path.join(SHOPS_DIR, 'kuvee-test1')
    with open(CONFIG_FILE, "a") as yaml_file:
        yaml_file.write(yaml.dump(data, default_flow_style=False))
    for d in data:

        print(d, data[d], type(data))
    return web.Response(text=str(data))
