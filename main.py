from aiohttp import web
from config.routes import setup_routes
from config.models import init_pg, close_pg, tables, engine_pg
from config.settings import shopifyAuth_DIR, shopify_DIR, BASE_DIR, TEMPLATE_DIRS, APP_CONF
import asyncio, aiohttp_jinja2, jinja2
import sqlalchemy
import sys, os
import argparse

#command line parser
def parser(*args):
    parser = argparse.ArgumentParser(description='Main command for the app')
    parser.add_argument('option1', help='runs the local web server', \
                        default = 'run', nargs='?')
    parser.add_argument('option2', help='runs the local web server', \
                        default = None, nargs='?')
    args = parser.parse_args()
    if args.option1 == 'run':
        # not processed (for host and port)
        main(args.option2)
    elif args.option1 == 'migrate':
        create_tables(tables )

# called with migrate command
def create_tables(tables = tables):
    engine = engine_pg(APP_CONF['postgres']['url'])
    for table in tables:
        try:
            getattr(table, 'create')(engine)
            print('Table: {}; created.'.format(table))
        except sqlalchemy.exc.ProgrammingError as e:
            print('Problem creating table: {}'.format(table))
            print('Reason: {}'.format(e))
        print('_____________________________________')

def init():
    loop = asyncio.get_event_loop()
    # setup application and extensions
    app = web.Application(loop=loop)

    app['config'] = APP_CONF

    def null_join(value, sep):
        return sep.join('' if v is None else str(v) for v in value)

    jinja_args = {
        'block_start_string': '<%',
        'block_end_string': '%>',
        'variable_start_string': '<<',
        'variable_end_string': '>>',
        'line_statement_prefix': '#',
        'line_comment_prefix': '##',
        'loader': jinja2.FileSystemLoader(TEMPLATE_DIRS),
        'filters': {
            'null_join': null_join,
        },
    }

    # setup Jinja2 template renderer
    #loader=jinja2.FileSystemLoader(TEMPLATE_DIRS)
    aiohttp_jinja2.setup(
    app, **jinja_args)

    # create connection to the database
    app.on_startup.append(init_pg)
    # shutdown db connection on exit
    app.on_cleanup.append(close_pg)
    # setup views and routes
    setup_routes(app)

    return app

# Creates the app for gunicorn
def run_gunicorn():
    app = init()
    return app

# App used by gunicorn
app = run_gunicorn()


# Starts the web server
def main(argv):
    app = init()
    web.run_app(app,  host=app['config']['host'],\
                port=app['config']['port'])

if __name__ == "__main__":
    parser(sys.argv[1:])
