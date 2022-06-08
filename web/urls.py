from web.apps import APP_NAME
from django.urls import path
from web import views,apis
app_name=APP_NAME

urlpatterns = [
    path('',views.HomeView.as_view(),name="home"),
    path('bus/<int:pk>/',views.BusView.as_view(),name="bus"),
    path('com_server/<int:pk>/',views.ComServerView.as_view(),name="comserver"),
    path('feeder/<int:pk>/',views.FeederView.as_view(),name="feeder"),
]
