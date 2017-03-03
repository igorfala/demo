from views import index
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_static('/static/',
                      path=BASE_DIR + '/static',
                      name='static')
