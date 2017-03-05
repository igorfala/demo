from config.settings import STATIC_DIR
import shopifyAuth.views as shopifyAuth_v
import shopify.views as shopify_v

# routes for shopifyAuth
shopifyAuth_rt = [
        ('GET', '/',        shopifyAuth_v.index,  'a_index'),
        ('GET', '/connect_shopify/{shop}',        shopifyAuth_v.connect_shopify,  'a_connect_shopify'),
        ('GET', '/auth/shopify/callback',        shopifyAuth_v.callback_shopify,  'a_callback_shopify'),
        ('GET', '/post_it/{code}',        shopifyAuth_v.post_it,  's_post'),
        ('POST', '/post_to',        shopifyAuth_v.post_to,  's_post_to'),

        ]

# routes for shopify
shopify_rt = [
        ('GET', '/shop',        shopify_v.index,  's_index'),
        ]

# all the routes
# for new apps create new route list
# then add it to routes: routes+=new_rt_list
routes = shopifyAuth_rt + shopify_rt

# route dispatch
def setup_routes(app):
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    app.router.add_static('/static/',
                      path=STATIC_DIR,
                      name='static')
