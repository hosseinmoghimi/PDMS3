# Phoenix
Project Manager
Doctor Assistant
Market
Accounting
Transport


create a venv:
```bash
python -m venv venv
```
activate it in linux:
```bash
source ./venv/bin/avtivate
```
or activate it in windows:
```bash
./venv/Scripts/avtivate.bat
```
install requirement:
```python
pip install -r requirements.txt
```

put your site root address,'/' , '/phoenix/' eg:
```python
echo "SITE_URL='/'" >> phoenix/settings_pars.py
```
or for special subdomain (for example '/phoenix/'):

```python
echo "SITE_URL='/phoenix/'" >> phoenix/server_settings.py
```
generate and view secret key:
```python
rm phoenix/secret_key.py
echo "SECRET_KEY = 'yj)%c-)__z_null-_l-ned!$6*cs)_=w@g&t=0vj^wg)knwm3z'" >> phoenix/secret_key.py
python manage.py djecrety
```

fill and copy this file as /PATH_TO_YOUR_APP_FOLDER/phoenix/settings_server.py
```python

DEBUG=True
# DEBUG=False



import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
YEAR_ADDED=0


SECRET_KEY='-+(&pe9ld9unwos@077r(cg#_)1$^l0c##+%gpy@&95da$=_hp'
SITE_URL='/'
PUSHER_IS_ENABLE=False
PUBLIC_ROOT=BASE_DIR
MYSQL=False
ALLOWED_HOSTS = ['*']





DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db9.sqlite3',
    # }
    
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': os.path.join(os.path.join(BASE_DIR, 'phoenix'),'secret_mysql.cnf'),

            },
        }
}

TIME_ZONE = 'Asia/Tehran'

STATIC_ROOT=os.path.join(PUBLIC_ROOT,'staticfiles')
MEDIA_ROOT=os.path.join(PUBLIC_ROOT,'media')
STATIC_URL = SITE_URL+'static/'
MEDIA_URL =  SITE_URL+'media/'


```

copy and put it in specific file:
```bash
vi phoenix/secret_key.py
```


put my sql db credential in files like right below:

```
[client]
database = your_database_name
host = your_host_name
user = your_user_name
password = your_password
default-character-set = utf8
```
for production:
```bash
rm phoenix/secret_my_sql.cnf
echo "[client]">> phoenix/secret_my_sql.cnf
echo "database = your_database_name">> phoenix/secret_my_sql.cnf
echo "host = your_host_name">> phoenix/secret_my_sql.cnf
echo "user = your_user_name">> phoenix/secret_my_sql.cnf
echo "password = your_password">> phoenix/secret_my_sql.cnf
echo "default-character-set = utf8" >> phoenix/secret_my_sql.cnf
```



migrate : 
```python
python manage.py migrate
```

create superuser : 
```python
python manage.py createsuperuser
```

collectstatic : 
```python
python manage.py collectstatic
```

https://tonyteaches.tech/django-nginx-uwsgi-tutorial/



```bash
cp ./server/phoenix.ini /etc/uwsgi/sites/phoenix.ini
cp ./server/phoenix /etc/nginx/sites-available/phoenix
```



test uwsgi:
```bash
uwsgi --http :8000 --module /home/leo/phoenix4/phoenix.wsgi
```


deploy: 
```bash
sudo vi /home/leo/phoenix/uwsgi_params
```



```bash
sudo vi /home/leo/phoenix/phoenix_uwsgi.ini
```
#copy phoenix_uwsgi.ini





```bash
sudo vi /etc/nginx/sites-available/phoenix.conf
```
#copy phoenix.conf




```bash
sudo ln -s /etc/nginx/sites-available/phoenix.conf /etc/nginx/sites-enabled/
```


uwsgi --socket phoenix.sock --module phoenix.wsgi --chmod-socket=666


```bash
uwsgi --ini phoenix_uwsgi.ini
```



vassals

```bash
cd /home/leo/phoenix/venv/
mkdir vassals
sudo ln -s /home/leo/phoenix/phoenix_uwsgi.ini /home/leo/phoenix/venv/vassals/
```



```bash
uwsgi --emperor /home/leo/phoenix/venv/vassals --uid www-data --gid www-data
```





```bash
sudo vi /etc/systemd/system/emperor.uwsgi.service
```
#copy emperor.uwsgi.service



```bash
systemctl enable emperor.uwsgi.service
systemctl start emperor.uwsgi.service
```


restart service:
```bash
systemctl restart emperor.uwsgi.service
sudo /etc/init.d/nginx restart
```
