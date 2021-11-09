from django.urls import path
from .apps import APP_NAME
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path("",(views.BasicViews().home),name="home"),
]
