from aiohttp import web, ClientSession, BasicAuth
from shopifyAuth.models import shops, shop_users
import shopifyAuth.models
import aiohttp_jinja2

#example
@aiohttp_jinja2.template('index.html')
async def img(request):
    async with request.app['db'].acquire() as conn:
        #cursor = await conn.execute(db.question.select())
        #records = await cursor.fetchall()
        return
#example
async def proxy(request):
    context = {}
    response = aiohttp_jinja2.render_template('index.html', request, context)
    #response.headers['Content-Type'] = 'application/liquid'
    print(response, response.headers)
    return response

#Displays shop Info to liquid
async def shop_info(request):
    try:
        data = dict(request.rel_url.query)
        shop = data['shop']
    except Exception as e:
        print(e)
        return web.Response(text='NOT AUTHORIZED', status=404)

    # checking that it's coming from shopify
    if not '.myshopify.com' in shop:
        return web.Response(text='NOT AUTHORIZED', status=404)
    shop = shop.split('.myshopify.com')[0]

    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(shops.select().where(shops.c.shop == shop))
        row = await cursor.fetchone()
        token = row.access_token
        context = await get_shop_info(shop, token)
        response = aiohttp_jinja2.render_template('shop.html', request, context)
        response.headers['Content-Type'] = 'application/liquid'
        return response

# Call to the API to get Shop Info
async def get_shop_info(shop, token):

    async with ClientSession() as session:
        url = 'https://{}.myshopify.com/admin/products.json'.format(shop)
        headers = {'X-Shopify-Access-Token': token }

        async with session.get(url, headers=headers) as resp:
            return await resp.json()
