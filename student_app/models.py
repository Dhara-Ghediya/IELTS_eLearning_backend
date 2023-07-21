from django.db import models
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator, RegexValidator
from rest_framework.authtoken.models import Token
import binascii
import os

# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator])
    password = models.CharField(max_length=250, 
                                validators=[MaxLengthValidator(limit_value=250), 
                                            MinLengthValidator(limit_value=8, 
                                                               message="Password must be at least 8 characters")])
    
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    type_of_user = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50, validators=[RegexValidator(regex=r'^[a-zA-Z]+$', 
                                                                            message="First Name must be Alphabetic")])
    last_name = models.CharField(max_length=50, validators=[RegexValidator(regex=r'^[a-zA-Z]+$', 
                                                                           message="Last Name must be Alphabetic")])
    age = models.IntegerField(validators=[RegexValidator(regex=r'^\S[0-9]{0,3}$',
                                                                       message="Entered Invalid Age")])
    mobile = models.CharField(max_length=12)
    gender = models.CharField(max_length=50, validators=[RegexValidator(regex=r'^[a-zA-Z]+$', 
                                                                         message="Gender must be Alphabetic")])
    country = models.CharField(max_length=50, validators=[RegexValidator(regex=r'^[a-zA-Z]+$', 
                                                                         message="Country must be Alphabetic")])
    def __str__(self):
        return self.type_of_user+ ": "+ self.first_name+ " "+ self.last_name
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
    question = models.ForeignKey(writings_model, verbose_name = "Question", on_delete = models.CASCADE)
    answer = models.TextField(verbose_name = "Answer from student")
    checkedQuestion=models.BooleanField(default=False)
    studentObtainMarks = models.IntegerField(default=0)
    
class StudentReadingAnswers(models.Model):
    #question = models.ForeignKey(writings_model, verbose_name = "Question", on_delete = models.CASCADE)
    firstQuestionAnswer = models.TextField(verbose_name = "First Question Answer from student")
    secondQuestionAnswer = models.TextField(verbose_name = "Second Question Answer from student")
    thirdQuestionAnswer = models.TextField(verbose_name = "Third Question Answer from student")
    fourthQuestionAnswer = models.TextField(verbose_name = "Fourth Question Answer from student")
    fifthQuestionAnswer = models.TextField(verbose_name = "Fifth Question Answer from student")
    checkedQuestion=models.BooleanField(default=False)
    studentObtainMarks = models.IntegerField(default=0)

class StudentListeningAnswer(models.Model):
    #question = models.ForeignKey(listing_model, verbose_name = "Question")
    answer=models.TextField(verbose_name="student answer")
    checkedQuestion=models.BooleanField(default=False)
    studentObtainMarks = models.IntegerField(default=0)
    
class StudentSpeakingAnswer(models.Model):
    #question = models.ForeignKey(reading_model, verbose_name="Question")
    answer = models.AutoField(verbose_name="student Answer") 
    checkedQuestion=models.BooleanField(default=False)
    studentObtainMarks = models.IntegerField(default=0)


class Permissions(models.Model):
    permissionName=models.CharField(verbose_name="permission name")
class MemberGroup(models.Model):
    group_name = models.CharField(max_length=100)