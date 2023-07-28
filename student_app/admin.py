from django.contrib import admin
from .models import *
# from django.contrib.auth.models import

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
admin.site.register(UserModel, UserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_of_user', 'first_name', 'last_name', 'country']
admin.site.register(Profile, ProfileAdmin)

class StudentTestSubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestamp', 'student']
admin.site.register(StudentTestSubmitModel, StudentTestSubmissionAdmin)

class StudentWritingAnswersAdmin(admin.ModelAdmin):
    list_display = ['id','get_name', 'timestamp', 'answer', 'checkedQuestion', 'studentObtainMarks']
    def get_name(self, obj):
        return obj.testNumber.student.username
admin.site.register(StudentWritingAnswers,StudentWritingAnswersAdmin)
admin.site.register(StudentReadingAnswers)
admin.site.register(StudentListeningAnswer)
admin.site.register(StudentSpeakingAnswer)

admin.site.register(Permissions)
admin.site.register(MemberGroup)
admin.site.register(UserTokens)