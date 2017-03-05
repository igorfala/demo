from aiohttp import web
import shopifyAuth.models
import aiohttp_jinja2

#async def index(request):
#    return web.Response(text='Hello World')

@aiohttp_jinja2.template('shop.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        #cursor = await conn.execute(db.question.select())
        #records = await cursor.fetchall()
        return

async def proxy(request):
    print(request.url, type(request.url))
    print(request.headers, type(request.headers))
    print(request.match_info, type(request.match_info))
    print(request.rel_url.query_string, type(request.rel_url.query_string))
    print(request.content, type(request.content))
    context = {'questions': request.content}
    response = aiohttp_jinja2.render_template('index.html', request, context)
    response.headers['Content-Type'] = 'application/liquid'

    return response
