import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask

from app.config.env_vars import LOG_DIR, LOG_FILE


def setup_logger(app: Flask) -> None:
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=100240, backupCount=10)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Logger is set up.")
