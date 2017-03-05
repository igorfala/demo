from aiohttp import web
import shopifyAuth.models
import aiohttp_jinja2

#async def index(request):
#    return web.Response(text='Hello World')

@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        #cursor = await conn.execute(db.question.select())
        #records = await cursor.fetchall()
        questions = {'q1':"random question",
                    'q2':"another random question"}
        return {'questions': questions}
