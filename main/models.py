from django.db import models
from django.conf import settings

from .base_models import *
from abstract.models import *


class UserDataApp(object):
    
    class Meta:
        app_label = 'user_data'
        
        
class SimpleModel(models.Model):
    
    name = models.CharField(max_length=300)
    
    class Meta:
        
        abstract = True
    
    def __str__(self):
        
        return self.name


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
    category = models.CharField(max_length=3, choices=CATEGORIES, default='', blank=True)
    
    list_description = models.TextField(default='', blank=True)
    detail_description = models.TextField(default='', blank=True)
    
    model_number = models.CharField(max_length=300, default='', blank=True)
    lens_size = models.PositiveIntegerField(default=0, blank=True)
    
    available_qty = models.PositiveIntegerField('Available quantity', default=0, blank=True)
    
    image_url = models.URLField(default='', blank=True)
    main_image = models.ImageField(upload_to='product-images', null=True, blank=True)
    
    detail_images = models.ManyToManyField('main.Image', blank=True, related_name='products')
    
    price = models.FloatField(default=0.0, blank=True)
    discounted_price = models.FloatField(default=0.0, blank=True)
    
    published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_top_rated = models.BooleanField(default=False)
    
    brand = models.ForeignKey('main.Brand', null=True, blank=True, related_name='products', on_delete=models.SET_NULL)
    frame_type = models.ForeignKey('main.FrameType', null=True, blank=True, related_name='products', on_delete=models.SET_NULL)
    type = models.ForeignKey('main.ProductType', null=True, blank=True, related_name='products', on_delete=models.SET_NULL)
    colors = models.ManyToManyField('main.Color', blank=True, related_name='products')
    
    def __str__(self):
        
        return self.name
        
        
class Brand(TimeStampedModel, SimpleModel):
    
    pass
        
        
class Color(TimeStampedModel, SimpleModel):
    
    pass
        
        
class FrameType(TimeStampedModel, SimpleModel):
    
    pass
    

class ProductType(TimeStampedModel, SimpleModel):
    
    pass

        
class ProductReview(BaseProductReview, TimeStampedModel):
    
    name = models.CharField(max_length=300, default='', blank=True)
    email = models.EmailField()
    
    rating = models.PositiveIntegerField(default=0)
    
    content = models.TextField(default='', blank=True)
    
    product = models.ForeignKey(Product, null=True, blank=True, related_name='reviews', on_delete=models.CASCADE)
    
    class Meta(TimeStampedModel.Meta):
        
        ordering = ('-created',)
        
    def __str__(self):
        
        return f'{ self.name }\'s review ({ self.rating }/5)'
        
        
class Cart(UserDataApp, models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='cart', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, through='user_data.CartProduct')
    
    def __str__(self):
        
        return f"{ self.user }'s cart ({ self.products.count() } products added)"
    
    
class Wishlist(UserDataApp, models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='wishlist', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, related_name='wishlists')
    
    def __str__(self):
        
        return f"{ self.user }'s wishlist ({ self.products.count() } products added)"


class CartProduct(UserDataApp, BaseCartProduct, models.Model):
    
    cart = models.ForeignKey(Cart, related_name='cart_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_products', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, null=True, related_name='cart_products', on_delete=models.CASCADE)
    
    qty = models.PositiveIntegerField('Quantity', default=0)
    
    def __str__(self):
        
        return f"{ self.cart.user }'s cart item (Product: { self.product }, Qty: { self.qty })"


class Image(BaseImage, models.Model):
    
    name = models.CharField(max_length=300, default='', blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='images')
    
    def __str__(self):
        
        return self.name or getattr(self.image, 'name', 'Unnamed image')
        
    class Meta:
        
        ordering = ('order',)
