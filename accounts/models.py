from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps

from main.models import *

import json


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, *args, **kwargs):
        
        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, *args, **kwargs):

        user = self.create_user(email, password=password)

        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    
    STATUSES = (
        ('I', 'Inactive'),  # Signed up but haven't set up account
        ('U', 'Unverifed'), # Set up account but haven't verified yet
        ('A', 'Active'), # Regular functioning account status
        ('S', 'Suspended'), # Suspended by an admin
        ('D', 'Deleted') # Partially deleted
    )
    
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=1, default='I', choices=STATUSES)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField('Last active', auto_now=True)

    timezone = models.CharField(max_length=100, default='', blank=True)

    activation_key = models.CharField(max_length=300, null=True, blank=True)
    activation_key_send_time = models.DateTimeField(null=True, blank=True)

    password_reset_key = models.CharField(max_length=300, null=True, blank=True)
    password_reset_send_time = models.DateTimeField(null=True, blank=True)

    first_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    
    # Google fields
    google_id = models.CharField(max_length=300, default='', blank=True)
    is_google_account = models.BooleanField(default=False)
    image_url = models.URLField(default='', blank=True)
    
    # Facebook fields
    is_facebook_account = models.BooleanField(default=False)
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    username = None
    objects = UserManager()
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:

        ordering = ('first_name', 'last_name')

    def __str__(self):

        return self.full_name or self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def as_light_dict(self):

        return {
            'id': self.id,

            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name
        }
        
    @property
    def full_name(self):

        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)

        if self.first_name:
            return self.first_name

        if self.last_name:
            return self.last_name

        return ''
        
    @property
    def readable_format(self):
        
        full_name = self.full_name
        
        if full_name:
            return full_name
            
        return self.email
        
    def toggle_suspension(self):

        if self.status == 'S':

            if self.invitation_key:
                self.status = 'N'

            elif self.activation_key:
                self.status = 'U'

            else:
                self.status = 'A'

        else:
            self.status = 'S'

        self.save()
        
    def as_json_dict(self):
         
        return json.dumps({
            'id': self.id,
            'name': self.full_name,
            'email': self.email
        })


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    
    if created:
        
        Cart.objects.create(user=instance)
        Wishlist.objects.create(user=instance)
