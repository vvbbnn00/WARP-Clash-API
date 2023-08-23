import os

SECRET_KEY = os.environ.get('SECRET_KEY') or None
REQUEST_RATE_LIMIT = os.environ.get('REQUEST_RATE_LIMIT') or 0
RANDOM_COUNT = os.environ.get('RANDOM_COUNT') or 10
LOSS_THRESHOLD = os.environ.get('LOSS_THRESHOLD') or 10
DELAY_THRESHOLD = os.environ.get('DELAY_THRESHOLD') or 500
PORT = os.environ.get('PORT') or 3000
HOST = os.environ.get('HOST') or '0.0.0.0'
