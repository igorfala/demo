from config.settings import STATIC_DIR
import aioApp.views as aioApp_v
import shopify.views as shopify_v

# routes for aioApp
aioApp_rt = [
        ('GET', '/',        aioApp_v.index,  'a_index'),
        ('GET', '/connect_shopify/{shop}',        aioApp_v.connect_shopify,  'a_connect_shopify'),
        ('GET', '/auth/shopify/callback',        aioApp_v.callback_shopify,  'a_callback_shopify'),
        ]

# routes for shopify
shopify_rt = [
        ('GET', '/shop',        shopify_v.index,  's_index'),
        ]

# all the routes
# for new apps create new route list
# then add it to routes: routes+=new_rt_list
routes = aioApp_rt + shopify_rt

# route dispatch
def setup_routes(app):
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    app.router.add_static('/static/',
                      path=STATIC_DIR,
                      name='static')
