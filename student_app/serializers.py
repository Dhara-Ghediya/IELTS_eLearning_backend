import json
from rest_framework import serializers
from rest_framework.fields import empty
from .models import *
# from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from teacher_app.serializers import WritingTestSerializer,ListeningTestSerializer,SpeakingTestSerializer,ReadingTestSerializer
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        
    def __init__(self, instance=None, data=..., **kwargs):
        try:
            data = data.copy()
            data['password'] = make_password(data['password'])
        except:
            pass
        super().__init__(instance, data, **kwargs)
        
class ProfileSerializer (serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
    # def __init__(self, instance=None, data=..., **kwargs):
    #     data = data.copy()
    #     print(self, data, kwargs, instance)
    #     data['user'] = UserModel.objects.filter(username=data['user']).first().pk
    #     print(data['user'])
    #     super().__init__(instance, data, **kwargs)

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)
    
    def save(self, **kwargs):
        print(kwargs)
        return super().save(**kwargs)
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'password']    

class StudentTestSubmitModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTestSubmitModel
        fields = "__all__"
class StudentWritingAnswersSerializer(serializers.ModelSerializer):
    # question=WritingTestSerializer()
    # testNumber=StudentTestSubmitModelSerializer
    class Meta:
        model = StudentWritingAnswers
        fields = ['testNumber', 'question', 'answer','checkedQuestion','studentObtainMarks']
class StudentReadingAnswersSerializer(serializers.ModelSerializer):
    # question=WritingTestSerializer()
    # testNumber=StudentTestSubmitModelSerializer
    class Meta:
        model = StudentReadingAnswers
        fields = ['testNumber', 'question', 'firstQuestionAnswer','secondQuestionAnswer','thirdQuestionAnswer','fourthQuestionAnswer','fifthQuestionAnswer','checkedQuestion','studentObtainMarks']


class StudentListeningAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentListeningAnswer
        fields = ['testNumber', 'question', 'answer','checkedQuestion','studentObtainMarks']

class StudentSpeakingAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSpeakingAnswer
        fields = '__all__'

class StudentWritingTestCheckSerializer(serializers.ModelSerializer):
    testNumber = StudentTestSubmitModelSerializer()
    question = WritingTestSerializer()
    student = serializers.SerializerMethodField()
    class Meta:
        model = StudentWritingAnswers
        fields = "__all__"
        read_only_fields = ['answer','student','question','testNumber','id']
            
    def get_student(self,obj):
        student=obj.testNumber.student
        return {"username":student.username,"email":student.email}
        