from .models import Profile
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['id','name','first_name','last_name','mobile','address','email','image','get_absolute_url','bio']
