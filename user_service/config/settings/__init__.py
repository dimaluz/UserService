import os

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


def reduce_path(file_name, times):
    result = os.path.realpath(file_name)
    for i in range(times):
        result = os.path.dirname(result)
    return result


ROOT = reduce_path(__file__, 3)
dotenv_path = os.path.join(ROOT, ".env")
load_dotenv(dotenv_path)

ENVS = ["DEVELOPMENT", "PRODUCTION", "STAGING"]

env = os.environ.get("DJANGO_ENV")

if env not in ENVS:
    error_message = "The currnet 'ENV' is {env} but must be one of {ENVS}"
    raise ImproperlyConfigured(error_message)

# match is a new keyword in Python 3.10, if your python version is less than 3.10, re-write this block with if-else
match env:
    case "DEVELOPMENT":
        from .dev import *
    case "PRODUCTION":
        from .prod import *
    case "STAGING":
        from .staging import *
