from django.contrib import admin
from .models import *

# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
admin.site.register(TeacherModel, TeacherAdmin)

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'country']
admin.site.register(TeacherProfile, TeacherProfileAdmin)
