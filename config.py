import os

DELAY_THRESHOLD = int(os.environ.get('DELAY_THRESHOLD')) if os.environ.get('DELAY_THRESHOLD') else 500
DO_GET_WARP_DATA = os.environ.get('DO_GET_WARP_DATA', 'true').lower() == 'true'
HOST = os.environ.get('HOST') or '0.0.0.0'
LOSS_THRESHOLD = int(os.environ.get('LOSS_THRESHOLD')) if os.environ.get('LOSS_THRESHOLD') else 10
PORT = int(os.environ.get('PORT')) if os.environ.get('PORT') else 3000
PROXY_POOL_URL = os.environ.get('PROXY_POOL_URL', 'https://getproxy.bzpl.tech/get/')
PUBLIC_URL = os.environ.get('PUBLIC_URL') or None
RANDOM_COUNT = int(os.environ.get('RANDOM_COUNT')) if os.environ.get('RANDOM_COUNT') else 10
REOPTIMIZE_INTERVAL = int(os.environ.get('REOPTIMIZE_INTERVAL', -1))
REQUEST_RATE_LIMIT = int(os.environ.get('REQUEST_RATE_LIMIT')) if os.environ.get('REQUEST_RATE_LIMIT') else 0
SECRET_KEY = os.environ.get('SECRET_KEY') or None
SHARE_SUBSCRIPTION = os.environ.get('SHARE_SUBSCRIPTION', 'false').lower() == 'true'
