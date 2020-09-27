from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status

from abstract.viewsets import CreateListRetrieveUpdateViewSet


User = get_user_model()


class LoginViewSet(CreateListRetrieveUpdateViewSet):
    
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    
    def validate_login(self, request, *args, **kwargs):
        
        if request.is_ajax():
            
            data = request.POST
            
            user = authenticate(username=data['email'], password=data['password'])
            print(user)
            
            if not user:
                return JsonResponse({'error': 'Invalid credentials. Please check if you typed your email and password correctly and try again'}, status=400)
                
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
