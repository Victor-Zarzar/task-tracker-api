import logging.config
import yaml
from pathlib import Path
from app.config.settings import settings


# Setup logger configuration
# This will load the logger configuration from a YAML file
def setup_logger():
    config_path = Path(__file__).resolve().parent.parent / "logger.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    log_level = settings.LOG_LEVEL.upper() if settings.LOG_LEVEL else "INFO"

    # Import to settings (.env)
    config["root"]["level"] = settings.LOG_LEVEL.upper()

    if "app" in config.get("loggers", {}):
        config["loggers"]["app"]["level"] = log_level

    logging.config.dictConfig(config)


setup_logger()
logger = logging.getLogger(__name__)
