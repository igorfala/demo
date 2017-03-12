from config.settings import APP_CONF

SHOPIFY_AUTH_URI = APP_CONF['shopify']['auth_uri'].format('{}',APP_CONF['shopify']['key'],\
                APP_CONF['shopify']['scope'], APP_CONF['shopify']['redirect_uri'], '{}', APP_CONF['shopify']['grant_options'])

def process_token_data(data):
    """
    checks if grant_options: per-user
    """
    shop_user_data = data.pop('associated_user', None)
    if shop_user_data:
        data['associated_user_id'] = shop_user_data['id']

    return  data, shop_user_data
