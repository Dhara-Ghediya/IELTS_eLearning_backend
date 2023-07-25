from rest_framework import serializers
from rest_framework.fields import empty
from .models import *
# from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

class TeacherRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherModel
        fields = '__all__'
        
    def __init__(self, instance=None, data=..., **kwargs):
        data = data.copy()
        # to encrypt the password
        data['password'] = make_password(data['password'])
        super().__init__(instance, data, **kwargs)
     
class TeacherProfileSerializer (serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = '__all__'
        
    # def __init__(self, instance=None, data=..., **kwargs):
    #     data = data.copy()
    #     data['user'] = TeacherModel.objects.filter(username=data['user']).first().pk
    #     super().__init__(instance, data, **kwargs)

    # def is_valid(self, *, raise_exception=False):
    #     return super().is_valid(raise_exception=raise_exception)
    
    # def save(self, **kwargs):
    #     return super().save(**kwargs)
 
class TeacherLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherModel
        fields = ['username', 'password'] 

class WritingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTests
        fields = "__all__"

    ### to get id using username 
    # def __init__(self, instance=None, data=..., **kwargs):
    #     data = data.copy()
    #     data['teacher'] = TeacherModel.objects.filter(username=data['teacher']).first().pk
    #     super().__init__(instance, data, **kwargs)
        
class ListeningTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningTests
        fields = "__all__"
    
class SpeakingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakingTests
        fields = "__all__"

class ReadingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingTests
        fields = "__all__"
        