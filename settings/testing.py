import dj_database_url 
from .base import *  # NOQA


SECRET_KEY = "CHANGEME!!!"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "CONN_MAX_AGE": 600,
        # number of seconds database connections should persist for
        "NAME": "KlimaatHelpdeskDev",
        "USER": "postgres",
        "HOST": "localhost",
        "PASSWORD": "Vfhsdbgtcfbt85456$%",
    },
    'defaultRender': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://klimaathelpdeskdev_user:jRrv7yfoUkVI5Xt437CU43PS9SfXEHlo@dpg-cvr7nsvgi27c738n8log-a.frankfurt-postgres.render.com/klimaathelpdeskdev',
        #default='postgresql://klimaathelpdeskdev_user:jRrv7yfoUkVI5Xt437CU43PS9SfXEHlo@dpg-cvr7nsvgi27c738n8log-a/klimaathelpdeskdev',
        conn_max_age=600
    )
}