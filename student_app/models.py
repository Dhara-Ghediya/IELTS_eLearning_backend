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
