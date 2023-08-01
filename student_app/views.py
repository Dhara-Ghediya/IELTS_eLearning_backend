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

class LoginView(APIView):

    def post(self, request):
        try: 
            user = UserModel.objects.filter(username= request.data['username']).first()
            if check_password(request.data['password'], user.password):
                # user = UserModel.objects.filter(username=request.data['username']).first()
                token = UserTokens.objects.update_or_create(user = user)
                serializer = {"username": user.username, "token": token[0].key}
                print("2")
                return Response(serializer, status = 201)
            else:
                return Response({'msg': 'Invalid credentials'}, status= 404)
        except Exception as e:
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

    def get(self, request, *args, **kwargs):
        check, obj = token_auth(request)
        if not check:
            return Response({'msg': obj}, status= 404)
        questions = []
        if WritingTests.objects.count() <= 2:
            questions = WritingTests.objects.all()
        else:
            questions = get_random_number_List(WritingTests, 2)  
        writingTestsSerializer = WritingTestSerializer(questions, many=True)
        return Response(writingTestsSerializer.data, status=200)
    
    
    def post(self, request, *args, **kwargs):
        check, obj = token_auth(request)
        if not check:
            return Response({'msg': obj}, status= 404)
        temp = dict(request.data)
        submitTest, _ = StudentTestSubmitModel.objects.get_or_create(student = obj.user)
        if submitTest:
            temp['testNumber'] = submitTest.id
            temp['question'] = int(temp['question'][0])
            temp['answer'] = temp['answer'][0]
            writingTestSerializer = StudentWritingAnswersSerializer(data = temp)
            if writingTestSerializer.is_valid():
                writingTestSerializer.save()
                return Response(writingTestSerializer.data, status=201)
            else:
                return Response({"details": writingTestSerializer.errors})
        return Response({"errors": "error while saving test. please try again"})
    
class ReadingTestView(APIView):
    
    def get(self, request, *args, **kwargs):
        check, obj = token_auth(request)
        if not check:
            return Response({'msg': obj}, status= 404)
        questions = []
        if ReadingTests.objects.count() <= 2:
            questions = ReadingTests.objects.all()
        else:
            questions = get_random_number_List(ReadingTests, 3)         
        readingTestsSerializer = ReadingTestSerializer(questions, many=True)
        return Response(readingTestsSerializer.data, status=200)
    
    def post(self, request, *args, **kwargs):
        check, obj = token_auth(request)
        if not check:
            return Response({'msg': obj}, status= 404)
        temp = dict(request.data)
        submitTest = StudentTestSubmitModel.objects.create(student = obj.user)
        if submitTest:
            temp['testNumber'] = submitTest.id
            temp['question'] = int(temp['question'][0])
            temp['answer'] = temp['answer'][0]
            readingTestSerializer = StudentReadingAnswersSerializer(data = temp)
            if readingTestSerializer.is_valid():
                readingTestSerializer.save()
                return Response(readingTestSerializer.data, status=201)
            else:
                return Response(readingTestSerializer.errors)
        return Response({"errors": "error while saving test. please try again"})
    
class ListingTestView(APIView):
    def get(self, request, *args, **kwargs):
        check, obj = token_auth(request)
        if not check:
            return Response({'msg': obj}, status= 404)
        questions = []
        if ListeningTests.objects.count() <= 2:
            questions = ListeningTests.objects.all()
        else:
            questions = get_random_number_List(ListeningTests, 1)   
        leashingTestsSerializer = ListeningTestSerializer(questions, many=True, context={"request": request})
        return Response(leashingTestsSerializer.data, status=200)
    
    def post(self, request, *args, **kwargs):
        check, obj = token_auth(request)
        if not check:
            return Response({'msg': obj}, status= 404)
        temp = dict(request.data)
        submitTest, _ = StudentTestSubmitModel.objects.get_or_create(student = obj.user)
        if submitTest:
            temp['testNumber'] = submitTest.id
            temp['question'] = int(temp['question'][0])
            temp['answer'] = temp['answer'][0]
            listingTestSerializer = StudentListeningAnswersSerializer(data = temp)
            if listingTestSerializer.is_valid():
                listingTestSerializer.save()
                return Response(listingTestSerializer.data, status=201)
            else:
                return Response(listingTestSerializer.errors)
        return Response({"errors": "error while saving test. please try again"})
    
class SpeakingTestView(APIView):
    def get(self, request, *args, **kwargs):
        check, obj = token_auth(request)
        if not check:
            return Response({'msg': obj}, status= 404)
        questions = []
        if SpeakingTests.objects.count() <= 2:
            questions = SpeakingTests.objects.all()
        else:
            questions = get_random_number_List(SpeakingTests, 1)   
        speakingTestsSerializer = SpeakingTestSerializer(questions, many=True, context={"request": request})
        return Response(speakingTestsSerializer.data, status=200)
     
    def post(self, request, *args, **kwargs):
        check, obj = token_auth(request)
        if not check:
            return Response({'msg': obj}, status= 404)
        temp = dict(request.data)
        submitTest, _ = StudentTestSubmitModel.objects.get_or_create(student = obj.user)
        if submitTest:
            temp['testNumber'] = submitTest.id
            temp['question'] = int(temp['question'][0])
            temp['answer'] = temp['answer'][0]
            speakingTestSerializer = StudentSpeakingAnswersSerializer(data = temp,context={"request": request})
            if speakingTestSerializer.is_valid():
                speakingTestSerializer.save()
                return Response(speakingTestSerializer.data, status=201)
            else:
                return Response(speakingTestSerializer.errors)
        return Response({"errors": "error while saving test. please try again"})

class StudentWritingTestAnswersLists(APIView):
    def get(self, request, *args, **kwargs):
        check, obj =token_auth(request)
        if not check:
            return Response({'msg': obj}, status= 404)
        answerList=StudentWritingAnswers.objects.filter(testNumber__student=obj.user)
        
        serializer=WritingTestAnswerListSerializer(answerList,many=True)
        return Response(serializer.data)
    
# ----------------------------------------------------------------
# return random test questions for test
def get_random_number_List(model, numberOfQuestions):
    List = []
    numberList = []
    idList = [x.id for x in model.objects.all()]
    while len(List) < numberOfQuestions:
            var = random.choice(idList)
            if var not in numberList:
                try:
                    List.append(model.objects.get(id = var))
                    numberList.append(var)
                except:
                    pass
    return List

# ----------------------------------------------------------------
# check any value is empty or not
def check_value_validation(dictValue):
    for i in dictValue.keys():
        if len(dictValue[i]) !=0 and str(dictValue[i][0]).strip() == "":
            return False, f'{i} is not a valid'
    return True, None

# ----------------------------------------------------------------
# Token authentication
def token_auth(request):
    token = request.headers.get('token',None)
    if token is None:
        return False,"please provide a token"
    try:
        user = UserTokens.objects.get(key=token)
        return True,user
    except UserTokens.DoesNotExist:
        return False,"token does not valid"
