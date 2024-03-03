"""

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.

"""
import logging
import time
from functools import wraps

from faker import Faker
from flask import Flask, request, make_response, current_app, render_template

from config import SECRET_KEY, REQUEST_RATE_LIMIT, SHARE_SUBSCRIPTION
from services.account import resetAccountKey, doUpdateLicenseKey
from services.common import getCurrentAccount
from services.subscription import generateClashSubFile, generateWireguardSubFile, generateSurgeSubFile, \
    generateShadowRocketSubFile, generateSingBoxSubFile

RATE_LIMIT_MAP = {}


def authorized(can_skip: bool = False):
    """
    All requests must be authorized
    :param can_skip: If true, the request can skip authorization when SHARE_SUBSCRIPTION is true
    :return:
    """

    def decorator(f):
        @wraps(f)
        def decoratedFunction(*args, **kwargs):
            # Skip authorization if the route can be shared
            if SHARE_SUBSCRIPTION and can_skip:
                return f(*args, **kwargs)

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
            return httpSubscription("shadowrocket")
        elif "v2ray" in user_agent:  # V2Ray
            return httpSubscription("shadowrocket")
        elif "quantumult" in user_agent:  # Quantumult
            return httpSubscription("clash")
        elif "surge" in user_agent:  # Surge
            return httpSubscription("surge")
        elif "sing-box" in user_agent:  # Sing Box
            return httpSubscription("sing-box")

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

    @app.route('/api/account/reset_key', methods=['POST'])
    @rateLimit()
    @authorized()
    def httpAccountResetKey():
        try:
            resetAccountKey(logger)
        except Exception as e:
            return {
                'code': 500,
                'message': str(e)
            }, 500
        return {
            'code': 200,
            'message': 'ok'
        }

    @app.route('/api/account/update_license', methods=['POST'])
    @rateLimit()
    @authorized()
    def httpAccountUpdateLicense():
        license_key = request.json.get('license_key')
        if not license_key:
            return {
                'code': 400,
                'message': 'License key is required'
            }, 400
        try:
            doUpdateLicenseKey(license_key, logger)
        except Exception as e:
            return {
                'code': 500,
                'message': str(e)
            }, 500
        return {
            'code': 200,
            'message': 'ok'
        }

    @app.route('/api/<string:sub_type>', methods=['GET'])
    @rateLimit()
    @authorized(can_skip=True)
    def httpSubscription(sub_type: str):
        user_agent = request.headers.get('User-Agent', 'unknown').lower()
        account = getCurrentAccount(logger)
        best = request.args.get('best', 'false').lower() == "true" or False
        random_name = request.args.get('randomName', 'false').lower() == "true" or False
        proxy_format = request.args.get('proxyFormat', 'full').lower()
        ipv6 = request.args.get('ipv6', 'false').lower() == "true" or False

        headers = {
            'Content-Type': 'application/x-yaml; charset=utf-8',
            "Subscription-Userinfo": f"upload=0; download={account.usage}; total={account.quota}; "
                                     f"expire=253388144714"
        }

        if sub_type == "clash":  # Clash

            # It seems that `dns` will cause problem in android.
            # So it is necessary to check if the user agent contains "android".
            # https://github.com/vvbbnn00/WARP-Clash-API/issues/74
            is_android = "android" in user_agent

            file_data = generateClashSubFile(account,
                                             logger,
                                             best=best,
                                             proxy_format=proxy_format,
                                             random_name=random_name,
                                             is_android=is_android,
                                             ipv6=ipv6)
            file_name = f'Clash-{fake.color_name()}.yaml'

        elif sub_type == "wireguard":  # Wireguard
            file_data = generateWireguardSubFile(account,
                                                 logger,
                                                 best=best,
                                                 ipv6=ipv6)
            file_name = f'WireGuard-{fake.lexify("????????????").lower()}.conf'

        elif sub_type == "surge":  # Surge
            file_data = generateSurgeSubFile(account,
                                             logger,
                                             best=best,
                                             random_name=random_name,
                                             proxy_format=proxy_format,
                                             ipv6=ipv6)
            file_name = f'Surge-{fake.color_name()}.conf'

        elif sub_type == 'shadowrocket':  # Shadowrocket
            file_data = generateShadowRocketSubFile(account,
                                                    logger,
                                                    best=best,
                                                    random_name=random_name,
                                                    ipv6=ipv6)
            file_name = f'Shadowrocket-{fake.color_name()}.conf'

        elif sub_type == 'sing-box':  # Sing Box
            file_data = generateSingBoxSubFile(account,
                                               logger,
                                               best=best,
                                               random_name=random_name,
                                               ipv6=ipv6)
            file_name = f'SingBox-{fake.color_name()}.json'

        # This might be deprecated in the future.
        elif sub_type == "only_proxies":  # Only proxies
            file_data = generateClashSubFile(account,
                                             logger,
                                             best=best,
                                             proxy_format='with_groups',
                                             random_name=random_name,
                                             ipv6=ipv6)
            file_name = f'Clash-{fake.color_name()}.yaml'

        else:
            return {
                'code': 400,
                'message': 'Unsupported sub type.'
            }, 400

        headers['Content-Disposition'] = f'attachment; filename="{file_name}"'
        response = make_response(file_data)
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
    run_app = createApp()
    run_app.run(host='0.0.0.0', port=5000, debug=True)
