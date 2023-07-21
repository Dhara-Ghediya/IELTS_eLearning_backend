from django.contrib import admin
from .models import *

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

admin.site.register(StudentWritingAnswers)
admin.site.register(StudentReadingAnswers)
admin.site.register(StudentListeningAnswer)
admin.site.register(StudentSpeakingAnswer)

admin.site.register(Permissions)
admin.site.register(MemberGroup)