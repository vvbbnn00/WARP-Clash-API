import time
from functools import wraps

from flask import Flask, request, make_response, current_app, render_template
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

    @app.route('/sub', methods=['GET'])
    def httpAutoSub():
        user_agent = request.headers.get('User-Agent', 'unknown').lower()
        # Automatically detect subscription type by user agent
        if "clash" in user_agent:  # Clash
            return httpSubscription("clash")
        elif "shadowrocket" in user_agent:  # Shadowrocket
            return httpSubscription("clash")
        elif "quantumult" in user_agent:  # Quantumult
            return httpSubscription("clash")
        elif "surge" in user_agent:  # Surge
            return httpSubscription("surge")

        # By default, return Clash
        return httpSubscription("clash")

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

    @app.route('/api/<string:sub_type>', methods=['GET'])
    @rateLimit()
    @authorized()
    def httpSubscription(sub_type: str):
        account = getCurrentAccount(logger)
        best = request.args.get('best', 'false').lower() == "true" or False
        random_name = request.args.get('randomName', 'false').lower() == "true" or False

        if sub_type == "clash":  # Clash
            fileData = generateClashSubFile(account, logger, best=best, only_proxies=False, random_name=random_name)
            headers = {
                'Content-Type': 'application/x-yaml; charset=utf-8',
                'Content-Disposition': f'attachment; filename=Warp-{fake.color_name()}.yaml',
                "Subscription-Userinfo": f"upload=0; download={account.usage}; total={account.quota}; "
                                         f"expire=253388144714"
            }
        elif sub_type == "wireguard":  # Wireguard
            fileData = generateWireguardSubFile(account, logger, best=best)
            headers = {
                'Content-Type': 'application/x-conf; charset=utf-8',
                'Content-Disposition': f'attachment; filename={fake.lexify("????????????").lower()}.conf'
            }
        elif sub_type == "surge":  # Surge
            fileData = generateSurgeSubFile(account, logger, best=best, random_name=random_name)
            headers = {
                'Content-Type': 'text/plain; charset=utf-8',
                'Content-Disposition': 'attachment; filename=warp.conf',
                "Subscription-Userinfo": f"upload=0; download={account.usage}; total={account.quota}; "
                                         f"expire=253388144714"
            }
        elif sub_type == "only_proxies":  # Only proxies
            fileData = generateClashSubFile(account, logger, best=best, only_proxies=True, random_name=random_name)
            headers = {
                'Content-Type': 'application/x-yaml; charset=utf-8',
                'Content-Disposition': f'attachment; filename=Warp-{fake.color_name()}.yaml',
                "Subscription-Userinfo": f"upload=0; download={account.usage}; total={account.quota}; "
                                         f"expire=253388144714"
            }
        else:
            return {
                'code': 400,
                'message': 'Unsupported sub type.'
            }, 400

        response = make_response(fileData)
        response.headers = headers

        return response


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
