from .base import * # NOQA
import pymysql

pymysql.install_as_MySQLdb()

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default':{
        'ENGINE' : 'django.db.backends.mysql',
        'NAME': 'wakenforest_blog_db',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '<正式数据库 ip>'
        'PORT': 3306,
        'CONN_MAX_AGE': 5*60,
        'OPTIONS': {'charset':'utf8mb4'}
    },
}