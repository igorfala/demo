from aioApp.views import index
from aioApp.settings import BASE_DIR

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_static('/static/',
                      path=BASE_DIR + '/static',
                      name='static')
