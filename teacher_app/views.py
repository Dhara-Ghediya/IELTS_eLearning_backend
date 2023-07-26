import re
import json
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
from django.core.files.storage import FileSystemStorage
# Create your views here.
# def home(request):
#     return render(request, 'index.html')
 
def imagefile_validator(value):
    # file_extension_validator = FileExtensionValidator(ALLOWED_EXTENSIONS_FOR_IMAGE)
    # file_extension_validator(value)
    if value.split('.')[-1] in ALLOWED_EXTENSIONS_FOR_IMAGE:
        return True
    else:
        return False
    # max_file_size_validator_for_image(value)

# to login for teacher
class TeacherLoginView(APIView):
    def post(self, request):
        if str(request.data['username']).strip() != "":
            pass
        else:
            return Response({'msg': 'Username is required'}, status = 404)
        if str(request.data['password']).strip() != "":
            pass
        else:
            return Response({'msg': 'password is required'}, status = 404)
        try: 
            user = TeacherModel.objects.filter(username = request.data['username']).first()
            # used to check encrypted password  
            if check_password(request.data['password'], user.password):
                request.session['teacher_user'] = user.username
                serializer = TeacherLoginSerializer(user)
                return Response(serializer.data, status = 201)
            else:
                return Response({'msg': 'Invalid credentials'}, status = 404)
        except Exception as e:
            return Response({'msg': 'You are not registered user!'}, status = 404)
        
# for logout (teachers)
class TeacherLogout(APIView):
    # permission_classes = (IsAuthenticated, )
    def post(self, request):
        if 'student_user' in request.session.keys():
            request.session.pop('teacher_user')
            return Response({'msg': 'Successfully Logout'}, status= 200)
        else:
            return Response({'msg': 'Already Logged out!'})
        
# for teacher regtistration
class TeacherRegisterView(APIView):
    def post(self, request):
        user = TeacherModel.objects.filter(username=request.data['username'])
        # validation 
        if user.exists():
            return Response({'msg': 'Registration already exists'}, status=404)
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
                    serializer = TeacherRegistrationSerializer(data=request.data, many=False)
                    if serializer.is_valid():
                        serializer
                        serializer.save()
                        return Response({'msg': 'User has been registered Successfully'}, status= 201)
                    else:
                        return Response(serializer.errors)
                else:
                    return Response({'msg': reg_errors})
            return Response({'msg': reg_errors})

# for teacher profile
class TeacherProfileView(APIView):
    def post(self, request):
        print("iin user...", request.data['user'])
        user = TeacherModel.objects.filter(id = request.data['user'])
        print("user", user)
        if user.exists():
            serializer = TeacherProfileSerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': "Your Profile has been saved!"}, status= 201)
            else:
                return Response(serializer.errors)
        else:
            return Response ({'msg': 'You are not registered! Please register first.'})

# to post questions of Writing Test (only teacher can post questions)
class WritingTestsView(APIView):
    def post(self, request):
        teacher = request.data.get('teacher')
        content = request.data.get('content', None)
        images = request.data.get('images', None)
        try:
            teacher = TeacherModel.objects.get(username=teacher).pk
        except TeacherModel.DoesNotExist:
            return Response({'msg': 'User not found!'}, status=404)
        
        if content is None:
            return Response({'msg': 'Content is missing in the request.'}, status = 400)
        
        if WritingTests.objects.filter(question=request.data['content']).exists():
            return Response({'msg': 'Question already exists!'}, status = 409)  
        else:
            try:
                image_url = None
                if images is not None:
                    image_folder = 'teacher_app/media/images/'
                    fs = FileSystemStorage(location=image_folder)
                    saved_image = fs.save(images.name, images)
                    image_url = fs.url(saved_image)
                    if not imagefile_validator(image_url):
                        return Response({'msg': 'Invalid Image Extension (only .png, .jpg, .jpeg, .webp allowed)!'}, status=400)
                question_data = {'content': content, 'images': image_url}
                serializer = WritingTestSerializer(data={'teacher': teacher, 'question': question_data})
                if serializer.is_valid():
                    serializer.save()   
                    return Response({'msg': 'Question has been added Successfully!'}, status=201)
                else:
                    return Response(serializer.errors, status=400)
            except Exception as e:
                return Response({"error": str(e)}, status=500)
        # # return Response({'msg': "Question already exists!"}, status=404)

# to post questions of Listening Test (only teacher can post questions)
class ListeningTestsView(APIView):
    def post(self, request):
        try:
            request.data['teacher'] = TeacherModel.objects.get(username=request.data['teacher']).pk
        except TeacherModel.DoesNotExist:
            return Response({'msg': 'User not found!'}, status=404)
        
        if ListeningTests.objects.filter(question=request.data['question']).exists():
            return Response({'msg': 'Question already exists!'}, status = 409)
        else:
            serializer = ListeningTestSerializer(data=request.data)
            if serializer.is_valid():
                print("if......")
                serializer.save()
                return Response({'msg':'Question has been added Successfully!'}, status=201)
            else:
                print("else..")
                return Response(serializer.errors, status= 404)
        # return Response({'msg': "Question already exists!"}, status=404)

# to post questions of Speaking Test (only teacher can post questions)
class SpeakingTestsView(APIView):
    def post(self, request):
        if SpeakingTests.objects.filter(question=request.data['question']).exists():
            return Response({'msg': 'Question already exists!'}, status = 409)
        else:
            serializer = SpeakingTestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Question has been added Successfully!'}, status=201)
            else:
                return Response(serializer.errors)

# to post questions of Reading Test (only teacher can post questions)            
class ReadingTestsView(APIView):
    def post(self, request):
        if ReadingTests.objects.filter(question=request.data['question']).exists():
            return Response({'msg': 'Question already exists!'}, status = 409)
        else:
            serializer = ReadingTestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Question has been added Successfully!'}, status=201)
            else:
                return Response(serializer.errors)