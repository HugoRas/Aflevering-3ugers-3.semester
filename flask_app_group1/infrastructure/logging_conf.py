import os
import logging
from logging.handlers import RotatingFileHandler


def _cfg_get(cfg, key):
    return cfg[key] if isinstance(cfg, dict) else getattr(cfg, key)


def setup_logging(cfg):
    log_dir = _cfg_get(cfg, "LOG_DIR")
    os.makedirs(log_dir, exist_ok=True)

    app_log_path = os.path.join(log_dir, "app.log")

    file_handler = RotatingFileHandler(
        app_log_path,
        maxBytes=1_000_000,
        backupCount=3,
    )
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    root = logging.getLogger()
    if not root.handlers:
        root.setLevel(logging.INFO)
        root.addHandler(file_handler)
        root.addHandler(console_handler)
