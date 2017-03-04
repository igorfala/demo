from aiohttp import web
from config.settings import CONFIG_DIR, APP_CONF, SHOPS_DIR
from aioApp.helpers.shopify import SHOPIFY_AUTH_URI
import aioApp.models
import aiohttp_jinja2
import yaml
import uuid
import os

@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        #cursor = await conn.execute(db.question.select())
        #records = await cursor.fetchall()
        questions = {'q1':"random question"}
        return {'questions': questions}

# redirects to shopify auth with shop name
async def connect_shopify(request):
    shop = request.match_info['shop']
    nonce = uuid.uuid4().hex
    SHOPIFY_AUTH_URL = SHOPIFY_AUTH_URI.format(shop, nonce)
    CONFIG_FILE = os.path.join(SHOPS_DIR, shop)
    with open(CONFIG_FILE, "w") as yaml_file:
        yaml_file.write(yaml.dump({"state": nonce}, default_flow_style=False))

    return web.Response(
        status=302,
        headers={
            'location': SHOPIFY_AUTH_URL,
        },
    )

# callback from shopify
async def callback_shopify(request):
    data = dict(request.rel_url.query)
    #validate the shop params
    nonce = data['state']
    shop = data['shop']
    if '.myshopify.com' in shop:
        shop = shop.split('.myshopify.com')[0]
        CONFIG_FILE = os.path.join(SHOPS_DIR, shop)
        with open(CONFIG_FILE) as f:
            SHOP_CONF = yaml.safe_load(f)
        if SHOP_CONF['state'] == nonce:
            with open(CONFIG_FILE, "w") as yaml_file:
                yaml_file.write(yaml.dump(SHOP_CONF, default_flow_style=False))
            return web.Response(text=str(data))

    return web.Response(text='ERROR')
    #async with aiohttp.ClientSession() as session:
    #    data = None
    #    async with session.post('https://api.github.com/events') as resp:
    #        print(resp)
