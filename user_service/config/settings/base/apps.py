# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps:
    "rest_framework",
    "rest_framework_simplejwt",
    # Custom apps:
    "event_bus",
    "users",
]
