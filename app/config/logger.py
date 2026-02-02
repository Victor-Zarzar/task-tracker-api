import logging.config
from pathlib import Path

import yaml

from app.config.settings import settings


def setup_logger():
    config_path = Path(__file__).resolve().parent.parent.parent / "logger.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    log_level = settings.LOG_LEVEL.upper() if settings.LOG_LEVEL else "INFO"

    config["root"]["level"] = settings.LOG_LEVEL.upper()

    if "app" in config.get("loggers", {}):
        config["loggers"]["app"]["level"] = log_level

    logging.config.dictConfig(config)


setup_logger()
logger = logging.getLogger(__name__)
