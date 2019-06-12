from .base import * # NOQA

DEBUG = False

ALLOWED_HOSTS = ['wakenforest.com']

DATABASES = {
    'default':{
        'ENGINE' : 'django.db.backends.mysql',
        'NAME': 'wakenforest_blog_db',
        'USER': 'root',
        'HOST': '<正式数据库 ip>'
        'PORT': 3306,
        'CONN_MAX_AGE': 5*60,
        'OPTIONS': {'charset':'utf8mb4'}
    },
}