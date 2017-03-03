from aiohttp import web
import models
import aiohttp_jinja2

#async def index(request):
#    return web.Response(text='Hello World')

@aiohttp_jinja2.template('base.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        #cursor = await conn.execute(db.question.select())
        #records = await cursor.fetchall()
        questions = {'q1':"random question"}
        return {'questions': questions}
