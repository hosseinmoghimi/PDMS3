from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import os
DEBUG=True
COM_SERVER_IS_CONNECTED=True
SECRET_KEY = 'django-insecure-2qnnu#vd@82**fu^yoacg6tm#s!-qt+1e+c!#4#@=_19b1&48e'


EMAIL_PORT=0
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_HOST=''
SEND_EMAIL=''

SITE_URL="/"
STATIC_URL = SITE_URL+'static/'
MEDIA_URL = SITE_URL+'media/'
ADMIN_URL = SITE_URL+'admin/'

STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]

PUBLIC_ROOT = os.path.join(BASE_DIR,"public")
STATIC_ROOT = os.path.join(PUBLIC_ROOT,"staticfiles")
MEDIA_ROOT = os.path.join(PUBLIC_ROOT,"media")

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db2.sqlite3',
    }
}


