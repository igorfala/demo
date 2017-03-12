import os
import yaml

DEBUG = True # Set False in Production, True in stagging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
shopifyAuth_DIR = os.path.join(BASE_DIR, 'shopifyAuth')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
shopify_DIR = os.path.join(BASE_DIR, 'shopify')
CONFIG_DIR = os.path.join(BASE_DIR, "config")
#SHOPS_DIR = os.path.join(CONFIG_DIR, "shops")

TEMPLATE_DIRS = [os.path.join(BASE_DIR, "templates" ),
                os.path.join(shopifyAuth_DIR, "templates" ),\
                os.path.join(shopify_DIR, "templates" ),\
                ]

# load config from yaml file in current dir
with open(os.path.join(CONFIG_DIR, 'main_config.yaml')) as f:
    APP_CONF = yaml.safe_load(f)
