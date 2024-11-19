import os

from .base import *


DEBUG = False

ALLOWED_HOSTS = ["example.com"]

SECRET_KEY = os.environ.get("SECRET_KEY")
