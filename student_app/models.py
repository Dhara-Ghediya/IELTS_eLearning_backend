from django.conf import settings
from django.db import models
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator, RegexValidator,MaxValueValidator,MinValueValidator
from rest_framework.authtoken.models import Token
from teacher_app.models import WritingTests,ReadingTests,ListeningTests,SpeakingTests
import binascii
import os
from rest_framework.authtoken.models import Token

class Permissions(models.Model):
    permissionName = models.CharField(verbose_name = "permission name", max_length = 180)
    timeStamp = models.DateTimeField(auto_now_add = True)
    
    def __str__(self) -> str:
        return self.permissionName
    
class MemberGroup(models.Model):
    group_name = models.CharField(max_length = 100)
    permissions = models.ManyToManyField(Permissions, blank=True)

    def __str__(self) -> str:
        return self.group_name
    
class UserModel(models.Model):
    username = models.CharField(max_length = 100)
    # membership = models.ForeignKey(MemberGroup, on_delete = models.CASCADE, default = MemberGroup.objects.first())
    email = models.EmailField(validators = [EmailValidator])
    password = models.CharField(max_length = 250, 
                                validators = [MaxLengthValidator(limit_value = 250), 
                                            MinLengthValidator(limit_value = 8, 
                                                               message = "Password must be at least 8 characters")])
    
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete = models.CASCADE)
    type_of_user = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50, validators = [RegexValidator(regex = r'^[a-zA-Z]+$', 
                                                                            message = "First Name must be Alphabetic")])
    last_name = models.CharField(max_length=50, validators = [RegexValidator(regex=r'^[a-zA-Z]+$', 
                                                                           message="Last Name must be Alphabetic")])
    age = models.IntegerField(validators=[RegexValidator(regex = r'^\S[0-9]{0,3}$',
                                                                       message="Entered Invalid Age")])
    mobile = models.CharField(max_length = 12)
    gender = models.CharField(max_length = 50, validators = [RegexValidator(regex = r'^[a-zA-Z]+$', 
                                                                         message = "Gender must be Alphabetic")])
    country = models.CharField(max_length = 50, validators = [RegexValidator(regex = r'^[a-zA-Z]+$', 
                                                                         message = "Country must be Alphabetic")])
    def __str__(self):
        return self.type_of_user + ": " + self.first_name+ " " + self.last_name
#add
# class Tokens(models.Model):
#     user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
#     key = models.CharField(("Key"), max_length=40, primary_key=True)
#     created = models.DateTimeField(("Created"), auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super().save(*args, **kwargs)

#     @classmethod
#     def generate_key(cls):
#         return binascii.hexlify(os.urandom(20)).decode()

#     def __str__(self):
#         return self.key

class StudentTestSubmitModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add = True)
    student = models.ForeignKey(UserModel, verbose_name = "student", on_delete = models.CASCADE)
    
class StudentWritingAnswers(models.Model):
    testNumber = models.ForeignKey(StudentTestSubmitModel,verbose_name = "test number that student submit",on_delete = models.CASCADE)
    question = models.ForeignKey(WritingTests, verbose_name = "Question", on_delete = models.CASCADE)
    answer = models.TextField(verbose_name = "Answer from student")
    timestamp = models.DateTimeField(auto_now_add = True)
    checkedQuestion = models.BooleanField(default = False)
    studentObtainMarks = models.IntegerField(default = 0)
    
class StudentReadingAnswers(models.Model):
    testNumber = models.ForeignKey(StudentTestSubmitModel,verbose_name = "test number that student submit",on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)
    question = models.ForeignKey(ReadingTests, verbose_name = "Question", on_delete = models.CASCADE)
    answer = models.JSONField()
    checkedQuestion = models.BooleanField(default = False)
    studentObtainMarks = models.IntegerField(default = 0)

class StudentListeningAnswer(models.Model):
    testNumber = models.ForeignKey(StudentTestSubmitModel,verbose_name = "test number that student submit",on_delete = models.CASCADE)
    question = models.ForeignKey(ListeningTests, verbose_name = "Question",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)
    answer = models.TextField(verbose_name = "student answer")
    checkedQuestion = models.BooleanField(default = False)
    studentObtainMarks = models.IntegerField(default = 0)
    
class StudentSpeakingAnswer(models.Model):
    testNumber = models.ForeignKey(StudentTestSubmitModel,verbose_name = "test number that student submit",on_delete = models.CASCADE)
    question = models.ForeignKey(SpeakingTests, verbose_name = "Question", on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)
    answer = models.FileField(verbose_name = "student Answer") 
    checkedQuestion = models.BooleanField(default = False)
    studentObtainMarks = models.IntegerField(default = 0)
class UserTokens(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(UserModel, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=("User")
    )
    created = models.DateTimeField(("Created"), auto_now_add=True)

    

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


    