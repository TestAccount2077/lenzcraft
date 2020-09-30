from django.contrib import admin

from .models import *


models = (
    # Product,
    Wishlist,
    Cart,
    CartProduct
)

for model in models:
    admin.site.register(model)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'price', 'type', 'model_number', 'brand', 'color', 'frame_type', 'category', 'image_url')
    list_editable = ('name', 'price', 'type', 'brand', 'color', 'frame_type', 'category', 'image_url')
    list_filter = ('type', 'brand', 'frame_type', 'category')
    list_display_links = ('model_number',)
