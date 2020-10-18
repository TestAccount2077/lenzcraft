from django.db import models
from django.conf import settings

from .base_models import *
from abstract.models import *


class Product(BaseProduct, TimeStampedModel):
    
    TYPES = (
        ('EG', 'Eyeglasses'),
        ('SG', 'Sunglasses')
    )
    
    CATEGORIES = (
        ('MN', 'Men'),
        ('WM', 'Women'),
        ('KD', 'Kids')
    )
    
    FRAME_TYPES = (
        ('RA', 'Rectangle Frames'),
        ('RN', 'Round Frames'),
        ('SQ', 'Square Frames'),
        ('RM', 'Rimless Frames')
    )
    
    REVERSED_CATEGORIES = {
        category[1]: category[0] for category in CATEGORIES
    }
    
    name = models.CharField(max_length=300, default='')
    type = models.CharField(max_length=3, choices=TYPES, default='', blank=True)
    category = models.CharField(max_length=3, choices=CATEGORIES, default='', blank=True)
    
    list_description = models.TextField(default='', blank=True)
    detail_description = models.TextField(default='', blank=True)
    
    model_number = models.CharField(max_length=300, unique=True, default='', blank=True)
    frame_type = models.CharField(max_length=2, choices=FRAME_TYPES, default='', blank=True)
    lens_size = models.PositiveIntegerField(default=0, blank=True)
    
    available_qty = models.PositiveIntegerField('Available quantity', default=0, blank=True)
    
    image_url = models.URLField(default='', blank=True)
    
    image = models.ImageField(upload_to='product-images', null=True, blank=True)
    
    price = models.FloatField(default=0.0, blank=True)
    discounted_price = models.FloatField(default=0.0, blank=True)
    
    published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_top_rated = models.BooleanField(default=False)
    
    brand = models.ForeignKey('main.Brand', null=True, blank=True, related_name='products', on_delete=models.SET_NULL)
    color = models.ForeignKey('main.Color', null=True, blank=True, related_name='products', on_delete=models.SET_NULL)
    
    def __str__(self):
        
        return self.name
        
        
class Brand(TimeStampedModel):
    
    name = models.CharField(max_length=300)
    
    def __str__(self):
        
        return self.name
        
        
class Color(TimeStampedModel):
    
    name = models.CharField(max_length=300)
    
    def __str__(self):
        
        return self.name

        
class ProductReview(TimeStampedModel):
    
    name = models.CharField(max_length=300, default='', blank=True)
    email = models.EmailField()
    
    rating = models.PositiveIntegerField(default=0)
    
    content = models.TextField(default='', blank=True)
    
    product = models.ForeignKey(Product, null=True, blank=True, related_name='reviews')
    
    class Meta(TimeStampedModel.Meta):
        
        ordering = ('-created',)
        
    def __str__(self):
        
        return f'{ self.name } review ({ self.stars }/5)'
        
        
class Cart(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='cart')
    products = models.ManyToManyField(Product, blank=True, through='main.CartProduct')
    
    def __str__(self):
        
        return f"{ self.user }'s cart ({ self.products.count() } products added)"
    
    
class Wishlist(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='wishlist')
    products = models.ManyToManyField(Product, blank=True, related_name='wishlists')
    
    def __str__(self):
        
        return f"{ self.user }'s wishlist ({ self.products.count() } products added)"


class CartProduct(BaseCartProduct, models.Model):
    
    cart = models.ForeignKey(Cart, related_name='cart_products')
    product = models.ForeignKey(Product, related_name='cart_products')
    
    qty = models.PositiveIntegerField('Quantity', default=0)
    
    def __str__(self):
        
        return f"{ self.cart.user }'s cart item (Product: { self.product }, Qty: { self.qty })"
