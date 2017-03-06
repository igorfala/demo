from aiohttp import web, ClientSession, BasicAuth
import shopifyAuth.models
import aiohttp_jinja2

#async def index(request):
#    return web.Response(text='Hello World')

@aiohttp_jinja2.template('index.html')
async def img(request):
    async with request.app['db'].acquire() as conn:
        #cursor = await conn.execute(db.question.select())
        #records = await cursor.fetchall()
        return

async def proxy(request):
    print(request.url, type(request.url))
    print(request.headers, type(request.headers))
    print(request.match_info, type(request.match_info))
    print(request.rel_url.query_string, type(request.rel_url.query_string))
    print((await request.text()), type(await request.text()))
    context = {'questions': (await request.text())}
    print(context)
    response = aiohttp_jinja2.render_template('index.html', request, context)
    #response.headers['Content-Type'] = 'application/liquid'
    print(response, response.headers)
    return response

#Displays shop Info to liquid
async def shop_info(request):
    shop = request.match_info['shop']
    context = await get_shop_info(shop)
    print(context)
    context = {"shop":{"id":18156521,"name":"kuvee-test1","email":"ifala88@gmail.com","domain":"kuvee-test1.myshopify.com","created_at":"2017-03-01T16:28:35-05:00","province":"Massachusetts","country":"US","address1":"comm ave","zip":"02135","city":"Boston","source":None,"phone":"","updated_at":"2017-03-01T17:25:01-05:00","customer_email":None,"latitude":42.3399704,"longitude":-71.1670299,"primary_location_id":12996491,"primary_locale":"en","address2":None,"country_code":"US","country_name":"United States","currency":"USD","timezone":"(GMT-05:00) Eastern Time (US \u0026 Canada)","iana_timezone":"America\/New_York","shop_owner":"Igor Fala","money_format":"${{amount}}","money_with_currency_format":"${{amount}} USD","weight_unit":"lb","province_code":"MA","taxes_included":"false","tax_shipping":None,"county_taxes":true,"plan_display_name":"affiliate","plan_name":"affiliate","has_discounts":"false","has_gift_cards":"false","myshopify_domain":"kuvee-test1.myshopify.com","google_apps_domain":None,"google_apps_login_enabled":None,"money_in_emails_format":"${{amount}}","money_with_currency_in_emails_format":"${{amount}} USD","eligible_for_payments":true,"requires_extra_payments_agreement":"false","password_enabled":true,"has_storefront":true,"eligible_for_card_reader_giveaway":None,"finances":true,"setup_required":"false","force_ssl":true}}
    print(context)
    response = aiohttp_jinja2.render_template('shop.html', request, context)
    response.headers['Content-Type'] = 'application/liquid'
    return response

# Call to the API to get Shop Info
async def get_shop_info(shop):
    async with ClientSession() as session:
        url = 'https://{}.myshopify.com/admin/shop.json'.format(shop)
        headers = {'X-Shopify-Access-Token': 'ed50fb7a0f307024e7878bbf010d71a4'}

        async with session.get(url, headers=headers) as resp:
            return await resp.json()
