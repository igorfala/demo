from aiohttp import web, ClientSession, BasicAuth
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
    context = {'params': "some params"}
    response = aiohttp_jinja2.render_template('index.html', request, context)
    #response.headers['Content-Type'] = 'application/liquid'
    print(response, response.headers)
    return response

#Displays shop Info to liquid
async def shop_info(request):
    shop = request.match_info['shop']
    context = await get_shop_info(shop)
    print(context, type(context))
    response = aiohttp_jinja2.render_template('shop.html', request, context)
    #response.headers['Content-Type'] = 'application/liquid'
    return response

# Call to the API to get Shop Info
async def get_shop_info(shop):
    async with ClientSession() as session:
        url = 'https://{}.myshopify.com/admin/products.json'.format(shop)
        headers = {'X-Shopify-Access-Token': 'ed50fb7a0f307024e7878bbf010d71a4'}

        async with session.get(url, headers=headers) as resp:
            return await resp.json()
