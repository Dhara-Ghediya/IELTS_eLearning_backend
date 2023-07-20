from django.db import models

# Create your models here.
from teacher_app.models import writings_model,reading_model,speaking_model,listing_model
from django.core.validators import MaxLengthValidator,MinLengthValidator,EmailValidator
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
class StudentTestSubmitModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add = True)
    student = models.ForeignKey(UserModel, verbose_name = "student", on_delete = models.CASCADE)
    
class StudentWritingAnswers(models.Model):
    question = models.ForeignKey(writings_model, verbose_name = "Question", on_delete = models.CASCADE)
    answer = models.TextField(verbose_name = "Answer from student")
    checkedQuestion=models.BooleanField(default=False)
    studentObtainMarks = models.IntegerField(default=0)
    
class StudentReadingAnswers(models.Model):
    question = models.ForeignKey(writings_model, verbose_name = "Question", on_delete = models.CASCADE)
    firstQuestionAnswer = models.TextField(verbose_name = "First Question Answer from student")
    secondQuestionAnswer = models.TextField(verbose_name = "Second Question Answer from student")
    thirdQuestionAnswer = models.TextField(verbose_name = "Third Question Answer from student")
    fourthQuestionAnswer = models.TextField(verbose_name = "Fourth Question Answer from student")
    fifthQuestionAnswer = models.TextField(verbose_name = "Fifth Question Answer from student")
    checkedQuestion=models.BooleanField(default=False)
    studentObtainMarks = models.IntegerField(default=0)

class StudentListeningAnswer(models.Model):
    question = models.ForeignKey(listing_model, verbose_name = "Question")
    answer=models.TextField(verbose_name="student answer")
    checkedQuestion=models.BooleanField(default=False)
    studentObtainMarks = models.IntegerField(default=0)
    
class StudentSpeakingAnswer(models.Model):
    question = models.ForeignKey(reading_model, verbose_name="Question")
    answer = models.AutoField(verbose_name="student Answer") 
    checkedQuestion=models.BooleanField(default=False)
    studentObtainMarks = models.IntegerField(default=0)