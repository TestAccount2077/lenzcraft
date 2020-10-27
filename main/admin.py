from django.contrib import admin

from .models import *

# Site info
site = admin.site

site.site_header = 'Lenzcraft Admin Panel'
site.site_title = 'Lenzcraft Admin'
site.index_title = 'Lenzcraft Admin'

models = (
    Wishlist,
    Cart,
    CartProduct,
    Brand,
    Color
)

for model in models:
    admin.site.register(model)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'price', 'discounted_price', 'type', 'model_number', 'brand', 'color', 'frame_type', 'category', 'is_featured', 'is_top_rated', 'image_url')
    list_editable = ('name', 'price', 'discounted_price', 'type', 'brand', 'color', 'frame_type', 'category', 'is_featured', 'is_top_rated', 'image_url')
    list_filter = ('type', 'brand', 'frame_type', 'category', 'is_featured', 'is_top_rated')
    list_display_links = ('model_number',)
    search_fields = ('name', 'model_number', 'brand__name', 'color__name', 'frame_type', 'category', 'type', 'list_description', 'detail_description')
