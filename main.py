from aiohttp import web
from config.routes import setup_routes
from config.models import init_pg, close_pg
from config.settings import shopifyAuth_DIR, shopify_DIR, BASE_DIR, TEMPLATE_DIRS, APP_CONF
import asyncio, aiohttp_jinja2, jinja2
import sys, os

def init(loop):
    # setup application and extensions
    app = web.Application(loop=loop)

    app['config'] = APP_CONF

    # setup Jinja2 template renderer
    loader=jinja2.FileSystemLoader(TEMPLATE_DIRS)
    aiohttp_jinja2.setup(
    app, loader=loader)

    # create connection to the database
    app.on_startup.append(init_pg)
    # shutdown db connection on exit
    app.on_cleanup.append(close_pg)
    # setup views and routes
    setup_routes(app)

    return app

# Creates the app for gunicorn
def run_gunicorn():
    loop = asyncio.get_event_loop()
    app = init(loop)
    return app

# App used by gunicorn
app = run_gunicorn()


# Starts the web server
def main(argv):
    loop = asyncio.get_event_loop()
    app = init(loop)
    web.run_app(app,  host=app['config']['host'],\
                port=app['config']['port'])

if __name__ == "__main__":
    main(sys.argv[1:])
