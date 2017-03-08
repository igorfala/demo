from config.settings import STATIC_DIR
import shopifyAuth.views as shopifyAuth_v
import shopify.views as shopify_v

# routes for shopifyAuth
shopifyAuth_rt = [
    ('*', '/',                                shopifyAuth_v.auth,               'a_auth_shopify'),
    ('GET', '/connect_shopify/{shop}',        shopifyAuth_v.connect_shopify,    'a_connect_shopify'),
    ('GET', '/auth/shopify/callback',         shopifyAuth_v.callback_shopify,   'a_callback_shopify'),
        ]

# routes for shopify
shopify_rt = [
    ('GET', '/proxy/img',                     shopify_v.img,                    's_img'),
    ('GET', '/proxy/index',                         shopify_v.proxy,                  's_proxy'),
    ('GET', '/proxy/shop_info',        shopify_v.shop_info,              's_shop_info'),
    ]

# all the routes
# for new apps create new route list
# then add it to routes: routes+=new_rt_list
routes = shopifyAuth_rt
routes += shopify_rt

# route dispatch
def setup_routes(app):
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    app.router.add_static('/static/',
                      path=STATIC_DIR,
                      name='static')
