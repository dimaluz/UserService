from .basic import BASE_DIR


# Logging settings
FORMATTERS = (
    {
        "verbose": {
            "format": "[{levelname}] {asctime:s} {threadName} {thread:d} {module} {filename} {lineno:d} {name} {funcName} {process:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {asctime:s} {module} {filename} {lineno:d} {funcName} {message}",
            "style": "{",
        },
    },
)

HANDLERS = {
    "console_handler": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
    },
    "common_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": f"{BASE_DIR}/logs/userservice.log",
        "mode": "a",
        "encoding": "utf-8",
        "formatter": "simple",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
    "detailed_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": f"{BASE_DIR}/logs/userservice_detailed.log",
        "mode": "a",
        "formatter": "verbose",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
}

LOGGERS = (
    {
        "django": {
            "handlers": ["console_handler", "detailed_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["common_handler"],
            "level": "WARNING",
            "propagate": False,
        },
    },
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": FORMATTERS[0],
    "handlers": HANDLERS,
    "loggers": LOGGERS[0],
}
