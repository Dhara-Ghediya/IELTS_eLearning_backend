from django.db import models
from .validators import *
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator, RegexValidator,MaxValueValidator,MinValueValidator
from django.core.validators import FileExtensionValidator
from rest_framework import exceptions
import binascii
import os
import datetime

def audiofile_validator(value):
    file_extension_validator = FileExtensionValidator(ALLOWED_EXTENSIONS)
    file_extension_validator(value)
    max_file_size_validator(value)

# model for teacher (user) registration 
class TeacherModel(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator])
    password = models.CharField(max_length=250, 
                                validators=[MaxLengthValidator(limit_value=250), 
                                            MinLengthValidator(limit_value=8, 
                                                               message="Password must be at least 8 characters")])
    def __str__(self):
        return self.username

# below model used to get more information about teacher (user)    
class TeacherProfile(models.Model):
    user = models.OneToOneField(TeacherModel, on_delete=models.CASCADE)
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
        return self.first_name+ " "+ self.last_name


# COURSES = (
#         ("writing", "Writing"),
#         ("listening", "Listening"),
#         ("speaking", "Speaking"),
#         ("reading", "Reading")
#     )

# model used to add (only teacher can add) questions for writingTest  
class WritingTests(models.Model):
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE)
    # que_type = models.CharField(max_length=50, choices=COURSES)
    timeStamp = models.DateTimeField(auto_now_add = True)
    question = models.JSONField()
    
    def __str__(self):
        return self.question.get('content1', '')
    
    def set_text_content(self, content):
        self.question['content1'] = content
        self.save()
        
    def add_image(self, img_url):
        if 'image' not in self.question:
            self.question['image'] = []
        self.question['image'].append(img_url)
        self.save()

# model used to add (only teacher can add) questions for listeningTest
class ListeningTests(models.Model):
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE)
    question = models.FileField(upload_to='audios/', blank=False, validators=[audiofile_validator])
    timeStamp = models.DateTimeField(auto_now_add = True)

# model used to add (only teacher can add) questions for speakingTest  
class SpeakingTests(models.Model):
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE)
    # que_type = models.CharField(max_length=50, choices=COURSES)
    question = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.question

# model used to add (only teacher can add) questions for readingTest  
class ReadingTests(models.Model):
    teacher = models.ForeignKey(TeacherModel, on_delete = models.CASCADE)
    question = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True)
    subQuestion = models.JSONField()
    
    def __str__(self):
        return self.question
    
class TeacherTokens(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(TeacherModel, related_name='auth_token',
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

