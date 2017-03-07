from config.settings import APP_CONF

SHOPIFY_AUTH_URI = 'https://kuvee-test1.myshopify.com/admin/oauth/authorize?client_id=a8f7f0db93780b7ba2e731fe95cbacd6&scope=read_content,\
            write_content&redirect_uri=https://kuveedemo.herokuapp.com/auth/shopify/callback&state= 5cd8521d85ad41b796c11213ef7c1bee&grant_options[]='

SHOPIFY_AUTH_URI = APP_CONF['shopify']['auth_uri'].format('{}',APP_CONF['shopify']['key'],\
                APP_CONF['shopify']['scope'], APP_CONF['shopify']['redirect_uri'], '{}', APP_CONF['shopify']['grant_options'])

def process_token_data(data):
    #check if grant_options: per-user

    shop_user_data = data.pop('associated_user', None)
    if shop_user_data:
        data['associated_user_id'] = shop_user_data['id']

    return  data, shop_user_data
