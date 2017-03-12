from config.settings import STATIC_DIR
import shopifyAuth.views as shopifyAuth_v
import shopify.views as shopify_v

# all the routes
# for new apps import the views and add routes to the list
routes = [
    # routes for shopifyAuth
    #('method(s)', 'path',                    'handler',                         'name')
    ('*', '/',                                shopifyAuth_v.auth,               'a_auth_shopify'),
    ('GET', '/connect_shopify/{shop}',        shopifyAuth_v.connect_shopify,    'a_connect_shopify'),
    ('GET', '/auth/shopify/callback',         shopifyAuth_v.callback_shopify,   'a_callback_shopify'),
    # routes for shopify
    ('GET', '/img',                           shopify_v.img,                    's_img'),
    ('GET', '/index',                         shopify_v.index,                  's_index'),
    ('GET', '/shop_info/{shop}',              shopify_v.shop_info,              's_shop_info'),
    # routes for the proxy app should be of format: /proxy/route
    ('GET', '/proxy/test',                    shopify_v.test,                   's_test'),
    ]

# route dispatch
def setup_routes(app):
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    app.router.add_static('/static/',
                      path=STATIC_DIR,
                      name='static')
