import time
from functools import wraps

from flask import Flask, request, make_response, current_app, render_template, redirect, url_for
from config import SECRET_KEY, REQUEST_RATE_LIMIT
from services.subscription import generateClashSubFile, generateWireguardSubFile, generateSurgeSubFile
from services.common import *
from faker import Faker

RATE_LIMIT_MAP = {}


def authorized():
    """
    All requests must be authorized
    :return:
    """

    def decorator(f):
        @wraps(f)
        def decoratedFunction(*args, **kwargs):

            key = request.headers.get('X-Api-Key') or request.args.get('key')

            if key == SECRET_KEY or not SECRET_KEY:
                return f(*args, **kwargs)
            else:
                return {
                    'code': 403,
                    'message': 'Unauthorized'
                }, 403

        return decoratedFunction

    return decorator


def rateLimit(limit: int = REQUEST_RATE_LIMIT):
    """
    Rate limit decorator
    :param limit:
    :return:
    """

    def decorator(f):
        @wraps(f)
        def decoratedFunction(*args, **kwargs):

            remote_addr = request.headers.get('X-Forwarded-For') or request.remote_addr

            try:
                if remote_addr not in RATE_LIMIT_MAP:
                    RATE_LIMIT_MAP[remote_addr] = time.time()

                if RATE_LIMIT_MAP[remote_addr] + limit > time.time():
                    return {
                        'code': 429,
                        'message': 'Too Many Requests'
                    }, 429
                else:
                    RATE_LIMIT_MAP[remote_addr] = time.time()
            except Exception as e:
                current_app.logger.warning(e)
                RATE_LIMIT_MAP[remote_addr] = time.time()

            return f(*args, **kwargs)

        return decoratedFunction

    return decorator


def attachEndpoints(app: Flask):
    """
    Attach endpoints to app
    :param app:
    :return:
    """
    logger = app.logger
    logger.setLevel(logging.INFO)
    fake = Faker()

    @app.route('/')
    def httpIndex():
        return render_template('index.html')

    @app.route('/api/account', methods=['GET'])
    @rateLimit()
    @authorized()
    def httpAccount():
        account = getCurrentAccount(logger)
        return {
            'code': 200,
            'message': 'ok',
            'data': account.__dict__
        }

    @app.route('/api/clash', methods=['GET'])
    @rateLimit()
    @authorized()
    def httpClash():
        account = getCurrentAccount(logger)
        best = request.args.get('best') or False
        random_name = request.args.get('randomName').lower() == "true" or False

        fileData = generateClashSubFile(account, logger, best=best, random_name=random_name)

        headers = {
            'Content-Type': 'application/x-yaml; charset=utf-8',
            'Content-Disposition': f'attachment; filename=Clash-{fake.color_name()}.yaml',
            "Subscription-Userinfo": f"upload=0; download={account.usage}; total={account.quota}; expire=253388144714"
        }

        response = make_response(fileData)
        response.headers = headers

        return response
    
    @app.route('/clash', methods=['GET'])
    @rateLimit()
    @authorized()
    def httpClashDefault():
        request.args = request.args.copy()
        request.args['best'] = 'false'
        request.args['randomName'] = 'true'
        httpClash()

    @app.route('/api/wireguard', methods=['GET'])
    @rateLimit()
    @authorized()
    def httpWireguard():
        account = getCurrentAccount(logger)
        best = request.args.get('best') or False

        fileData = generateWireguardSubFile(account, logger, best=best)

        headers = {
            'Content-Type': 'application/x-conf; charset=utf-8',
            'Content-Disposition': f'attachment; filename={fake.lexify("????????????").lower()}.conf'
        }

        response = make_response(fileData)
        response.headers = headers

        return response
    
    @app.route('/wireguard', methods=['GET'])
    @rateLimit()
    @authorized()
    def httpWireguardDefault():
        request.args = request.args.copy()
        request.args['best'] = 'false'
        return httpWireguard()


    @app.route('/api/only_proxies', methods=['GET'])
    @rateLimit()
    @authorized()
    def httpOnlyProxies():
        account = getCurrentAccount(logger)
        best = request.args.get('best') or False
        random_name = request.args.get('randomName').lower() == "true" or False

        fileData = generateClashSubFile(account, logger, best=best, only_proxies=True, random_name=random_name)

        response = make_response(fileData)
        headers = {
            'Content-Type': 'application/x-yaml; charset=utf-8',
            'Content-Disposition': f'attachment; filename=Clash-{fake.color_name()}.yaml',
            "Subscription-Userinfo": f"upload=0; download={account.usage}; total={account.quota}; expire=253388144714"
        }

        response.headers = headers

        return response

    @app.route('/api/surge', methods=['GET'])
    @rateLimit()
    @authorized()
    def httpSurge():
        account = getCurrentAccount(logger)
        best = request.args.get('best') or False
        random_name = request.args.get('randomName').lower() == "true" or False

        fileData = generateSurgeSubFile(account, logger, best=best, random_name=random_name)

        headers = {
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Disposition': 'attachment; filename=surge.conf',
            "Subscription-Userinfo": f"upload=0; download={account.usage}; total={account.quota}; expire=253388144714"
        }

        response = make_response(fileData)
        response.headers = headers

        return response
    
    @app.route('/surge', methods=['GET'])
    @rateLimit()
    @authorized()
    def httpSurgeDefault():
        request.args = request.args.copy()
        request.args['best'] = 'false'
        request.args['randomName'] = 'true'
        return httpSurge()

def createApp(app_name: str = "web", logger: logging.Logger = None) -> Flask:
    """
    Create Flask app
    :param app_name:
    :param logger:
    :return:
    """
    if logger is None:
        logger = logging.getLogger()
    app = Flask(app_name)

    # Replace the default logger
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)
    for handler in logger.handlers:
        app.logger.addHandler(handler)
    app.logger.setLevel(logger.level)

    attachEndpoints(app)
    return app


if __name__ == '__main__':
    runApp = createApp()
    runApp.run(host='0.0.0.0', port=5000, debug=True)
