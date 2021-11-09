from django.urls import path
from .apps import APP_NAME
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path('',(views.BasicViews().home),name="home"),
    path('bus_monitoring/<int:bus_id>/',login_required(views.BasicViews().monitoring),name="bus_monitoring"),
    path('com_server/<int:pk>/',views.BasicViews().com_server,name="comserver"),
    path('node/<int:pk>/',views.BasicViews().node,name="node"),
    path('feeder/<int:pk>/',views.BasicViews().feeder,name="feeder"),
    path('bus/<int:pk>/',views.BasicViews().bus,name="bus"),
    path('area/<int:pk>/',views.BasicViews().area,name="area"),
    path('logs/',views.BasicViews().logs,name="logs"),
    path('get_feeder_data/',apis.BasicApi().get_feeder_data,name="get_feeder_data"),
    path('get_feeder_data/<int:pk>/',apis.BasicApi().get_feeder_data,name="get_feeder_data_get"),
    path('monitoring/',login_required(views.BasicViews().monitoring),name="monitoring"),
    path('demo/',views.BasicViews().demo,name="demo"),
    path('logs/',login_required(views.BasicViews().logs),name="logs"),
    path('log/<int:pk>/',views.BasicViews().log,name="log"),
    path('get_analog_data/',login_required(apis.BasicApi().get_analog_data),name="get_analog_data"),
    path('get_bus_data/',login_required(apis.BasicApi().get_bus_data),name="get_bus_data"),
    path('data/',views.BasicViews().data,name="data"),
    path('circuit_breaker_toggle/',login_required(apis.BasicApi().circuit_breaker_toggle),name="circuit_breaker_toggle"),
    path('circuit_breaker_read/',login_required(apis.BasicApi().circuit_breaker_read),name="circuit_breaker_read"),
    path('add_input_command/',login_required(views.BasicViews().add_input_command),name="add_input_command"),
]
