import logging
from logging.config import dictConfig
import colorlog


_LOGGING_CONFIGURED = False


def configure_logging(level=logging.INFO):
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return  # Prevent duplicate handlers

    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "default": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": (
                    "[%(asctime)s] %(levelname)s | %(name)s: %(message)s"
                )
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": level,
            }
        },

        "root": {
            "handlers": ["console"],
            "level": level,
        },
    })

    _LOGGING_CONFIGURED = True
