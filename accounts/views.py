from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status

from abstract.viewsets import CreateListRetrieveUpdateViewSet

from .validators import *


User = get_user_model()


class LoginViewSet(CreateListRetrieveUpdateViewSet):
    
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    
    def validate_signup(self, request, *args, **kwargs):
        
        if request.is_ajax():
            
            data = request.POST
            
            user = User.objects.filter(email__iexact=data['email']).first()
            
            if user:
                return self._400('A user with this email already exists. Please log in instead')
            
            name = data['name']
            email = data['email']
            password = data['password']
            password_confirmation = data['password_confirmation']
            
            validator = UserValidator()
            
            email_is_valid = validator.validate_email(email)
            
            if not email_is_valid:
                return self._400('Email is invalid')
            
            split_name = name.split(' ', 2)
            
            first_name = middle_name = last_name = ''
            
            if len(name) == 1:
                first_name = name
                
            if len(name) == 2:
                first_name, last_name = split_name
                
            elif len(name) == 3:
                first_name, middle_name, last_name = split_name
            
            user = User(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                email=email,
                phone=data['phone']
            )
            
            password_error = validator.validate_password(user, password, password_confirmation)
            
            if password_error:
                return self._400(password_error)
            
            user.set_password(password)
            user.save()
            
            return JsonResponse({})
            
    def validate_login(self, request, *args, **kwargs):
        
        if request.is_ajax():
            
            data = request.POST
            
            user = authenticate(username=data['email'], password=data['password'])
            
            if not user:
                return self._400('Invalid credentials. Please check if you typed your email and password correctly and try again')
            
            if user.is_google_account:
                return self._400('This account is signed up via Google. You must log in with Google to proceed')
                
            login(request, user)
            
            return JsonResponse({})
            
    def validate_google_login(self, request, *args, **kwargs):
        
        if request.is_ajax():
            
            data = request.POST
            
            email = data['email']
            
            user = User.objects.filter(email__iexact=email).first()
            
            if not user:
                
                split_name = data['name'].split(' ', 1)
                
                if len(split_name) > 1:
                    first_name = split_name[0]
                    last_name = split_name[1]
                
                else:
                    first_name = data['name']
                
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    google_id=data['id'],
                    is_google_account=True,
                    image_url=data['imageUrl']
                )
            
            login(request, user)
            
            return JsonResponse({})
            
    def logout(self, request, *args, **kwargs):
        
        if request.is_ajax():
            
            user = request.user
            
            logout(request)
            
            return JsonResponse({})
