import os
import yaml

DEBUG = False # Set False in Production, True in stagging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# load config from yaml file in current dir
with open(os.path.join(BASE_DIR, "config/main_config.yaml")) as f:
    APP_CONF = yaml.safe_load(f)
