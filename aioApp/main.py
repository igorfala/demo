import asyncio, aiohttp_jinja2, jinja2
import yaml, sys, os
from aiohttp import web
from aioApp.routes import setup_routes
from aioApp.models import init_pg, close_pg
from aioApp.settings import CURR_DIR, BASE_DIR

def init(loop):
    # setup application and extensions
    app = web.Application(loop=loop)

    # load config from yaml file in current dir
    with open(os.path.join(BASE_DIR, "config/main_config.yaml")) as f:
        conf = yaml.safe_load(f)

    app['config'] = conf

    # setup Jinja2 template renderer
    loader=jinja2.FileSystemLoader(os.path.join(CURR_DIR, "templates" ))
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
