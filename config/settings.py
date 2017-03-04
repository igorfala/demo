import os
import yaml

DEBUG = False # Set False in Production, True in stagging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
aioApp_DIR = os.path.join(BASE_DIR, 'aioApp')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
shopify_DIR = os.path.join(BASE_DIR, 'shopify')

TEMPLATE_DIRS = [os.path.join(aioApp_DIR, "templates" ),\
                os.path.join(shopify_DIR, "templates" ),]

CONFIG_FILE = os.path.join(BASE_DIR, "config/main_config.yaml")

# load config from yaml file in current dir
with open(CONFIG_FILE) as f:
    APP_CONF = yaml.safe_load(f)
