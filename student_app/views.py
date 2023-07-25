import json
import re
import random
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from teacher_app.models import WritingTests,ListeningTests
# Create your views here.
# def home(request):
#     return render(request, 'index.html')
 
def check_user_login(view_func):
    def _wrapped_view(request, *args, **kwargs):
        print(request.request.session.keys())
        if 'student_user' in request.request.session.keys():
            
            return view_func(request, *args, **kwargs)
        else:
            
            return Response("login is required")
        
    return _wrapped_view

class LoginView(APIView):
    def post(self, request):
        try: 
            user = UserModel.objects.filter(username= request.data['username']).first()
            if check_password(request.data['password'], user.password):
                # user = UserModel.objects.filter(username=request.data['username']).first()
                request.session['student_user'] = user.username
                serializer = LoginSerializer(user)
                return Response(serializer.data, status= 201)
            else:
                return Response({'msg': 'Invalid credentials'}, status= 404)
        except Exception as e:
            print('Error', e)
            return Response({'msg': 'You are not registered user!'}, status= 404)

class Logout(APIView):
    # permission_classes = (IsAuthenticated, )
    def post(self, request):
        if 'student_user' in request.session.keys():
            request.session.pop('student_user')
            return Response({'msg': 'Successfully Logout'}, status= 200)
        else:
            return Response({'msg': 'Already Logged out!'})

class RegisterView(APIView):
    def post(self, request):
        print("Register View Started")
        user = UserModel.objects.filter(username = request.data['username'])
        # validation 
        if user.exists():
            return Response({'msg': 'Registration already exists'}, status= 404)
        else:
            reg_errors = []
            if not re.match(r'^(?![._])[a-zA-Z0-9_.]{5,20}$', request.data['username']):
                reg_errors.append({'username': ["1)Username must be 5-20 characters long",\
				"2) Username may only contain:", "- Uppercase and lowercase letters", "- Numbers from 0-9 and",\
				"- Special characters _.", "3) Username may not:Begin or finish with _ ,."]})
            else:
                if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', request.data['email']):
                    pass
                else:
                    reg_errors.append({'email': 'Invalid Email'})
                if re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$", request.data['password']):
                    pass
                else:
                    reg_errors.append({'password': ["at least one digit", "at least one uppercase letter", "at least one lowercase letter", "at least one special character[$@#]"]})
                if len(reg_errors)== 0:
                    print("call...")
                    serializer = RegistrationSerializer(data= request.data, many= False)
                    if serializer.is_valid():
                        serializer
                        serializer.save()
                        return Response({'msg': 'User has been registered Successfully'}, status= 201)
                    else:
                        return Response(serializer.errors)
                else:
                    return Response({'msg': reg_errors})
            return Response({'msg': reg_errors})

class ProfileView(APIView):
    def post(self, request):
        user = UserModel.objects.filter(username= request.data['user'])
        if user.exists():
            serializer = ProfileSerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': "Your Profile has been saved!"}, status= 201)
            else:
                return Response(serializer.errors)
        else:
            return Response ({'msg': 'You are not registered! Please register first.'})

class WritingTestView(APIView):
    @check_user_login
    def get(self, request, *args, **kwargs):
        questions = []
        if WritingTests.objects.count() <= 2:
            questions = WritingTests.objects.all()
        else:
            questions = get_random_number_List(WritingTests, 1)         
        writingTestsSerializer = WritingTestSerializer(questions, many=True)
        return Response(writingTestsSerializer.data)
    
    
    @check_user_login
    def post(self, request, *args, **kwargs):
        print(request.data.get("username", ""))
        print(request.session.get('student_user', "***"))
        temp = dict(request.data)
        submitTest, _ = StudentTestSubmitModel.objects.get_or_create(student = UserModel.objects.get(username = request.session.get('student_user', "***")))
        if submitTest:
            temp['testNumber'] = submitTest.id
            temp['question'] = int(temp['question'][0])
            temp['answer'] = temp['answer'][0]
            writingTestSerializer = StudentWritingAnswersSerializer(data = temp)
            if writingTestSerializer.is_valid():
                writingTestSerializer.save()
                return Response(writingTestSerializer.data)
            else:
                return Response(writingTestSerializer.errors)
        return Response({"errors":"error while saving test. please try again"})
    
class ReadingTestView(APIView):
    def get(self, request, *args, **kwargs):
        questions = []
        if ReadingTests.objects.count() <= 2:
            questions = ReadingTests.objects.all()
        else:
            questions = get_random_number_List(ReadingTests, 1)         
        readingTestsSerializer = ReadingTestSerializer(questions, many=True)
        return Response(readingTestsSerializer.data)
    def post(self, request, *args, **kwargs):
        temp = dict(request.data)
        submitTest, _ = StudentTestSubmitModel.objects.get_or_create(student = UserModel.objects.get(username = request.session.get('student_user', "***")))
        if submitTest:
            temp['testNumber'] = submitTest.id
            temp['question'] = int(temp['question'][0])
            temp['firstQuestionAnswer'] = temp['firstQuestionAnswer'][0]
            temp['secondQuestionAnswer'] = temp['secondQuestionAnswer'][0]
            temp['thirdQuestionAnswer'] = temp['thirdQuestionAnswer'][0]
            temp['fourthQuestionAnswer'] = temp['fourthQuestionAnswer'][0]
            temp['fifthQuestionAnswer'] = temp['fifthQuestionAnswer'][0]
            readingTestSerializer = StudentReadingAnswersSerializer(data = temp)
            if readingTestSerializer.is_valid():
                readingTestSerializer.save()
                return Response(readingTestSerializer.data)
            else:
                return Response(readingTestSerializer.errors)
        return Response({"errors":"error while saving test. please try again"})
    
# class ReadingTestsView(viewsets.ModelViewSet):
#     queryset = ReadingTests.objects.all()
#     serializer_class=ReadingTestSerializer
class ListingTestView(APIView):
    def get(self, request, *args, **kwargs):
        questions = []
        if ListeningTests.objects.count() <= 2:
            questions = ListeningTests.objects.all()
        else:
            questions = get_random_number_List(ListeningTests, 1)   
        leashingTestsSerializer = ListeningTestSerializer(questions, many=True,context={"request": request})
        return Response(leashingTestsSerializer.data)
    def post(self, request, *args, **kwargs):
        temp = dict(request.data)
        submitTest, _ = StudentTestSubmitModel.objects.get_or_create(student = UserModel.objects.get(username = request.session.get('student_user', "***")))
        if submitTest:
            temp['testNumber'] = submitTest.id
            temp['question'] = int(temp['question'][0])
            temp['answer'] = temp['answer'][0]
            listingTestSerializer = StudentListeningAnswersSerializer(data = temp)
            if listingTestSerializer.is_valid():
                listingTestSerializer.save()
                return Response(listingTestSerializer.data)
            else:
                return Response(listingTestSerializer.errors)
        return Response({"errors":"error while saving test. please try again"})
    
class SpeakingTestView(APIView):
    def get(self, request, *args, **kwargs):
        questions = []
        if SpeakingTests.objects.count() <= 2:
            questions = SpeakingTests.objects.all()
        else:
            questions = get_random_number_List(SpeakingTests, 1)   
        speakingTestsSerializer = SpeakingTestSerializer(questions, many=True, context={"request": request})
        return Response(speakingTestsSerializer.data)
    
    def post(self, request, *args, **kwargs):
        temp = dict(request.data)
        submitTest, _ = StudentTestSubmitModel.objects.get_or_create(student = UserModel.objects.get(username = request.session.get('student_user', "***")))
        if submitTest:
            temp['testNumber'] = submitTest.id
            temp['question'] = int(temp['question'][0])
            temp['answer'] = temp['answer'][0]
            speakingTestSerializer = StudentSpeakingAnswersSerializer(data = temp,context={"request": request})
            if speakingTestSerializer.is_valid():
                speakingTestSerializer.save()
                return Response(speakingTestSerializer.data)
            else:
                return Response(speakingTestSerializer.errors)
        return Response({"errors":"error while saving test. please try again"})
    
def get_random_number_List(model, numberOfQuestions):
    List = []
    numberList = []
    while len(List) < numberOfQuestions:
            var = random.randint(1, model.objects.count())
            if var not in numberList:
                try:
                    List.append(model.objects.get(id = var))
                    numberList.append(var)
                except:
                    pass
    return List