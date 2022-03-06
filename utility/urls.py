from .apps import APP_NAME
from django.urls import path
from . import apis
from django.contrib.auth.decorators import login_required


app_name=APP_NAME
urlpatterns = [
    path('send_mail/',login_required(apis.BasicApis().send_mail),name="send_mail")
]
