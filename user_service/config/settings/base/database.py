import os
import redis


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "NAME": os.environ.get("DB_NAME", "default_db"),
        "USER": os.environ.get("DB_USER", "user"),
        "PASSWORD": os.environ.get("DB_PASS", "password"),
    }
}

#REDIS as STORAGE
REDIS_CLIENT = redis.StrictRedis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=os.environ.get("REDIS_PORT", "6379"),
    password=os.environ.get("REDIS_PASSWORD", "password"),
    db=0,
    decode_responses=True,
)