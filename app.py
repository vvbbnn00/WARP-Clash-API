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
import argparse
import sys

from config import PORT, HOST
from utils.entrypoints import optimizeEntrypoints
from utils.logger import createLogger


def linuxStartWeb():
    """
    Start web service on linux
    :return:
    """
    from gunicorn.app.base import BaseApplication
    from services.web_service import createApp

    class FlaskGunicornApp(BaseApplication):
        def __init__(self, flaskapp, options=None):
            self.options = options or {}
            self.application = flaskapp
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items() if
                      key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    app = createApp("web")
    FlaskGunicornApp(app, options={
        "bind": f"{HOST}:{PORT}",
        "workers": 4,
        "worker_connections": 1000,
        "timeout": 30,
        "keepalive": 2
    }).run()


def main():
    """
    Main function
    :return:
    """
    parser = argparse.ArgumentParser(description="WARP Clash API")
    parser.add_argument("command", choices=["web", "background", "optimize"], help="Command to run")

    args = parser.parse_args()

    if args.command == "web":
        logger = createLogger("app_web")
        from services.web_service import createApp
        app = createApp("web", logger=logger)

        # If windows, use app.run()
        if sys.platform == "win32":
            app.run(host=HOST, port=PORT)
        # If linux, use gunicorn
        else:
            linuxStartWeb()

    elif args.command == "background":
        logger = createLogger("app_background")
        from services.scheduled_service import main
        main(logger=logger)

    elif args.command == "optimize":
        # Windows is not supported for this command
        if sys.platform == 'win32':
            print('This command is not supported on Windows.')
            return
        optimizeEntrypoints()


if __name__ == "__main__":
    main()
