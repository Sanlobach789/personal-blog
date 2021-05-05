from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from authapp.models import User


class UserAdmin(UserAdmin):
    pass


admin.site.register(User, UserAdmin)
