import argparse
import os
import sys

from config import PORT, HOST


def linux_start_web():
    from gunicorn.app.base import BaseApplication
    from services.web_service import create_app

    class FlaskGunicornApp(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items() if
                      key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    app = create_app("web")
    FlaskGunicornApp(app, options={
        "bind": f"{HOST}:{PORT}",
        "workers": 4,
        "worker_class": "gevent",
        "worker_connections": 1000,
        "timeout": 30,
        "keepalive": 2
    }).run()


def main():
    parser = argparse.ArgumentParser(description="WARP Clash API")
    parser.add_argument("command", choices=["web", "background", "optimize"], help="Command to run")

    args = parser.parse_args()

    if args.command == "web":
        from services.web_service import create_app
        app = create_app("web")

        # If windows, use app.run()
        if sys.platform == "win32":
            app.run(host=HOST, port=PORT)
        # If linux, use gunicorn
        else:
            linux_start_web()

    elif args.command == "background":
        from services.scheduled_service import main
        main()
    elif args.command == "optimize":
        # Run ./scripts/get_entrypoint.sh
        os.system("bash ./scripts/get_entrypoint.sh")


if __name__ == "__main__":
    main()
