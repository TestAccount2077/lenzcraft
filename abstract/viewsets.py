from django.utils.decorators import method_decorator
from django.http import JsonResponse

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status

from .utils import enable_traceback


@method_decorator(enable_traceback, name='dispatch')
class CreateListRetrieveUpdateViewSet(mixins.CreateModelMixin,
      mixins.ListModelMixin,
      mixins.RetrieveModelMixin,
      mixins.UpdateModelMixin,
      viewsets.GenericViewSet):
    
    _404 = lambda self, message: JsonResponse({'error': message}, status=status.HTTP_404_NOT_FOUND)
    _400 = lambda self, message: JsonResponse({'error': message}, status=status.HTTP_400_BAD_REQUEST)
    _403 = lambda self, message: JsonResponse({'error': message}, status=status.HTTP_403_FORBIDDEN)
