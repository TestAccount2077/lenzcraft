from django.contrib import admin

from .models import *
from user_data.models import *

# Site info
site = admin.site

site.site_header = 'Lenzcraft Admin Panel'
site.site_title = 'Lenzcraft Admin'
site.index_title = 'Lenzcraft Admin'

models = (
    Brand,
    Color,
    ProductReview,
    Image,
    Cart,
    Wishlist,
    CartProduct
)

for model in models:
    admin.site.register(model)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'price', 'discounted_price', 'type', 'model_number', 'brand', 'frame_type', 'category', 'is_featured', 'is_top_rated', 'image_url')
    list_editable = ('name', 'price', 'discounted_price', 'type', 'brand', 'frame_type', 'category', 'is_featured', 'is_top_rated', 'image_url')
    list_filter = ('type', 'brand', 'frame_type', 'category', 'is_featured', 'is_top_rated')
    list_display_links = ('model_number',)
    search_fields = ('name', 'model_number', 'brand__name', 'colors__name', 'frame_type', 'category', 'type', 'list_description', 'detail_description')
