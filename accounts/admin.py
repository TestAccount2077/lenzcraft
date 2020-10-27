from django import forms
from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils import timezone

from .models import *


class UserCreationForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('email',)
        
    def clean_password2(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        return password2

    def save(self, commit=True):
        
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
            
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):

        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('full_name', 'email', 'status', 'is_staff', 'timezone', 'last_login', 'created', 'modified')
    list_filter = ('is_admin', 'is_staff', 'status', 'last_login', 'created')
    list_editable = ('status',)
    ordering = ('-modified', '-created')
    
    fieldsets = (
        (
            None, {
                'fields': (
                    'first_name', 'middle_name', 'last_name',
                    'password', 'status',
                    'activation_key', 'activation_key_send_time',
                    'password_reset_key', 'password_reset_send_time', 'timezone',
                )
            }
        ),
        (
            'Personal info', {
                'fields': ('email',)
            }
        ),
        (
            'Permissions', {
                'fields': ('is_admin','is_staff',)
            }
        ),
    )
    
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )


admin.site.register(User, UserAdmin)
