from rest_framework import serializers
from rest_framework.fields import empty
from .models import *
# from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        
    def __init__(self, instance=None, data=..., **kwargs):
        data = data.copy()
        data['password'] = make_password(data['password'])
        super().__init__(instance, data, **kwargs)
        
class ProfileSerializer (serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
    def __init__(self, instance=None, data=..., **kwargs):
        data = data.copy()
        print(self, data, kwargs, instance)
        data['user'] = UserModel.objects.filter(username=data['user']).first().pk
        print(data['user'])
        super().__init__(instance, data, **kwargs)

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)
    
    def save(self, **kwargs):
        print(kwargs)
        return super().save(**kwargs)
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'password']    
