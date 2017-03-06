from aiohttp import web, ClientSession, BasicAuth
import shopifyAuth.models
import aiohttp_jinja2

#async def index(request):
#    return web.Response(text='Hello World')

@aiohttp_jinja2.template('index.html')
async def img(request):
    async with request.app['db'].acquire() as conn:
        #cursor = await conn.execute(db.question.select())
        #records = await cursor.fetchall()
        return

async def proxy(request):
    print(request.url, type(request.url))
    print(request.headers, type(request.headers))
    print(request.match_info, type(request.match_info))
    print(request.rel_url.query_string, type(request.rel_url.query_string))
    print((await request.text()), type(await request.text()))
    context = {'questions': (await request.text())}
    print(context)
    response = aiohttp_jinja2.render_template('index.html', request, context)
    #response.headers['Content-Type'] = 'application/liquid'
    print(response, response.headers)
    return response

#Displays shop Info to liquid
async def shop_info(request):
    shop = request.match_info['shop']
    context = await get_shop_info(shop)
    context = 'hi'
    print(context)
    response = aiohttp_jinja2.render_template('shop.html', request, context)
    #response.headers['Content-Type'] = 'application/liquid'
    return response

# Call to the API to get Shop Info
async def get_shop_info(shop):
    async with ClientSession() as session:
        url = 'https://{}.myshopify.com/admin/shop.json'.format(shop)
        headers = {'X-Shopify-Access-Token': 'dcb788bd7a97fade33553b35011391a7'}

        async with session.get(url, headers=headers) as resp:
            return await resp.json()
