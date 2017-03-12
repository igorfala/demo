from aiohttp import web, ClientSession, BasicAuth
from shopifyAuth.models import shops, shop_users
from shopify.helpers.proxy_check import proxy_signature_is_valid
from config.settings import APP_CONF
import aiohttp_jinja2

# page served in shopify
async def test(request):
    try:
        data = dict(request.rel_url.query)
        shop = data['shop']
    except Exception as e:
        print(e)
        return web.Response(text='NOT AUTHORIZED', status=404)

    # checking that it's coming from shopify
    if not '.myshopify.com' in shop:
        return web.Response(text='NOT AUTHORIZED', status=404)
    #print('proxy', proxy_signature_is_valid(data, APP_CONF['shopify']['secret']))
    if proxy_signature_is_valid(data, APP_CONF['shopify']['secret']):
        context = {}
        response = aiohttp_jinja2.render_template('test.html', request, context)
        response.headers['Content-Type'] = 'application/liquid'
        print(response, response.headers)
        return response
    else:
        print('didnt validate')
    return web.Response(text='NOT AUTHORIZED', status=404)

#Displays products Info from API queries.
async def shop_info(request):
    shop = request.match_info['shop']
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(shops.select().where(shops.c.shop == shop))
        row = await cursor.fetchone()
        token = row.access_token
        context = await get_shop_info(shop, token)
        print(context)
        response = aiohttp_jinja2.render_template('shop.html', request, context)
        #response.headers['Content-Type'] = 'application/liquid'
        return response

# Call to the API to get Shop Info
async def get_shop_info(shop, token):

    async with ClientSession() as session:
        url = 'https://{}.myshopify.com/admin/products.json'.format(shop)
        headers = {'X-Shopify-Access-Token': token }

        async with session.get(url, headers=headers) as resp:
            return await resp.json()


#example
@aiohttp_jinja2.template('index.html')
async def img(request):
    return

#example
async def index(request):
    context = {}
    response = aiohttp_jinja2.render_template('index.html', request, context)
    #response.headers['Content-Type'] = 'application/liquid'
    print(response, response.headers)
    return response
