from django.contrib import admin

from main.models import *


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    
    pass
    

models = (
    CartProduct,
    # CartAdmin,
    Wishlist
)

for model in models:
    admin.site.register(model)
