import os

SECRET_KEY = os.environ.get('SECRET_KEY') or None
REQUEST_RATE_LIMIT = int(os.environ.get('REQUEST_RATE_LIMIT')) if os.environ.get('REQUEST_RATE_LIMIT') else 0
RANDOM_COUNT = int(os.environ.get('RANDOM_COUNT')) if os.environ.get('RANDOM_COUNT') else 10
LOSS_THRESHOLD = int(os.environ.get('LOSS_THRESHOLD')) if os.environ.get('LOSS_THRESHOLD') else 10
DELAY_THRESHOLD = int(os.environ.get('DELAY_THRESHOLD')) if os.environ.get('DELAY_THRESHOLD') else 500
DO_GET_WARP_DATA = bool(os.environ.get('DO_GET_WARP_DATA')) or True
PORT = int(os.environ.get('PORT')) if os.environ.get('PORT') else 3000
HOST = os.environ.get('HOST') or '0.0.0.0'
PROXY_POOL_URL = os.environ.get('PROXY_POOL_URL', 'https://getproxy.bzpl.tech/get/')
PUBLIC_URL = os.environ.get('PUBLIC_URL') or None
SURGE_SUBSCRIPTION_URL = os.environ.get('SURGE_SUBSCRIPTION_URL') or '/api/surge'
