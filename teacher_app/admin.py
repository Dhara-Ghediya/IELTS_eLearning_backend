from django.contrib import admin
from .models import *

# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']
admin.site.register(TeacherModel, TeacherAdmin)

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'country']
admin.site.register(TeacherProfile, TeacherProfileAdmin)

class WriteTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'timeStamp', 'question']
admin.site.register(WritingTests, WriteTestAdmin)

class ListningTestsAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'timeStamp', 'question']
admin.site.register(ListeningTests, ListningTestsAdmin)

class SpeakingTestsAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'timeStamp', 'question']
admin.site.register(SpeakingTests, SpeakingTestsAdmin)

admin.site.register(ReadingTests)