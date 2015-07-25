import logging
from logging.handlers import RotatingFileHandler
import os
from park_api import env
from park_api.app import app

def main():
    log_path = os.path.join(env.APP_ROOT, "log", env.ENV + ".log")
    log_handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=1)
    log_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s "))
    app.logger.addHandler(log_handler)

    app.logger.addHandler(logging.StreamHandler())

    if env.is_production():
        app.logger.setLevel(logging.INFO)
        log_handler.setLevel(logging.INFO)

    app.run(**vars(env.SERVER_CONF))
