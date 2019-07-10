from .base import * # NOQA
import pymysql

pymysql.install_as_MySQLdb()

DEBUG = True
# DEBUG = False

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wakenforest_blog_db',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST':'127.0.0.1',
        'PORT':3306,
        
    }
}


# INSTALLED_APPS += [
#     'debug_toolbar',
# ]

# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]

# INTERNAL_IPS = ['127.0.0.1']