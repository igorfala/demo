from aioApp.views import index
from aioApp.settings import BASE_DIR, STATIC_DIR
import os

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_static('/static/',
                      path=STATIC_DIR,
                      name='static')
