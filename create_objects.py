import os
import django
import datetime
import random

os.environ['DJANGO_SETTINGS_MODULE'] = 'lenzcraft.settings'
django.setup()

from user_data.models import *
from accounts.models import *


users = User.objects.all()
created_cart_count = 0
created_wishlist_count = 0

for user in User.objects.all():
    
    _, cart_created = Cart.objects.get_or_create(user=user)
    created_cart_count += int(cart_created)
    
    _, wishlist_created = Wishlist.objects.get_or_create(user=user)
    created_wishlist_count += int(wishlist_created)
    
print(f'{ users.count() } users found\n{ created_cart_count } carts created\n{ created_wishlist_count } wishlists created')
