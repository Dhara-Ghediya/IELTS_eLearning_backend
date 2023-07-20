from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
admin.site.register(UserModel, UserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_of_user', 'first_name', 'last_name', 'country']
admin.site.register(Profile, ProfileAdmin)
