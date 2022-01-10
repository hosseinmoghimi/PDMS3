from .models import *
from rest_framework import serializers


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'title', 'device_name', 'status', 'persian_date_added']


class ComServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComServer
        fields = ['id', 'name']


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'region', 'gps']


class BusSerializer(serializers.ModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = Bus
        fields = ['id', 'name', 'area', 'get_edit_url', 'get_color', 'panel']
# class AnalogInputSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=AnalogInput
#         fields=['id','com_server','value']


class FeederSerializer(serializers.ModelSerializer):
    com_server = ComServerSerializer()
    area = AreaSerializer()

    class Meta:
        model = Feeder
        fields = ['id', 'name', 'bus_id', 'area', 'address', 'com_server']


class FeederFullSerializer(serializers.ModelSerializer):
    com_server = ComServerSerializer()
    area = AreaSerializer()

    class Meta:
        model = Feeder
        fields = ['id', 'name', 'bus_id', 'area', 'address', 'i_a', 'i_b', 'i_c','v_a','v_b','v_c',
                  'com_server', 'circuit_breaker_status', 'circuit_breaker_schematic']


class FeederSerializerForChart(serializers.ModelSerializer):
    com_server = ComServerSerializer()
    bus = BusSerializer()

    class Meta:
        model = Feeder
        fields = ['id', 'name', 'bus', 'panel','panel_for_bus_view',
                  'address',  'com_server', 'get_edit_url']
class CurrentTransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentTransformer
        fields=['value_i_a','value_i_b','value_i_c']