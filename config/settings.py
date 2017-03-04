import os
import yaml

DEBUG = False # Set False in Production, True in stagging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
aioApp_DIR = os.path.join(BASE_DIR, 'aioApp')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
shopify_DIR = os.path.join(BASE_DIR, 'shopify')

TEMPLATE_DIRS = [os.path.join(aioApp_DIR, "templates" ),\
                os.path.join(shopify_DIR, "templates" ),]

CONFIG_DIR = os.path.join(BASE_DIR, "config")
SHOPS_DIR = os.path.join(CONFIG_DIR, "shops")
# load config from yaml file in current dir
with open(os.path.join(CONFIG_DIR, 'main_config.yaml')) as f:
    APP_CONF = yaml.safe_load(f)
