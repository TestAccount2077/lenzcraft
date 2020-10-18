import locale

locale.setlocale(locale.LC_ALL, '')


class BaseProduct(object):
    
    @property
    def brand_name(self):
        return getattr(self.brand, 'name', '')
        
    @property
    def color_name(self):
        return getattr(self.color, 'name', '')
        
    def as_dict(self, user=None, **kwargs):
        
        price = self.formatted_price
        discounted_price = self.formatted_discounted_price
        
        DEFAULT_IMAGE_URL = 'https://lenzcraft.herokuapp.com/static/img/212X200/img2.jpg'
        
        data = {
            'id': self.id,
            'name': self.name,
            'type': self.get_type_display(),
            'category': self.get_category_display(),
            'model_number': self.model_number,
            'image_url': self.image.url if self.image else self.image_url or DEFAULT_IMAGE_URL,
            
            'price': self.price,
            'discounted_price': self.discounted_price,
            'formatted_price': discounted_price if self.discounted_price else price,
            'formatted_discounted_price': price if self.discounted_price else discounted_price,
            
            'published': self.published,
            'is_featured': self.is_featured,
            'is_top_rated': self.is_top_rated,
            
            'brand': self.brand_name,
            'color': self.color_name,
            'frame_type': self.get_frame_type_display(),
            
            'created_timestamp': self.created.timestamp(),
            'total_rating': self.total_rating,
            'reviews': [review.as_dict() for review in self.reviews.all()],
            'url': f'/products/{ self.id }/',
            'available_qty': self.available_qty,
            'in_stock': self.in_stock,
            'in_stock_label': self.in_stock_label,
            'qty': 0,
            'total_cost': 0,
            
            'list_description': self.list_description,
            'detail_description': self.detail_description
        }
        
        if user and user.is_authenticated:

            data.update({
                'in_cart': user.cart.cart_products.filter(product=self).exists(),
                'in_wishlist': user.wishlist.products.filter(id=self.id).exists()
            })
            
            cart_product = user.cart.cart_products.filter(product=self).first()
            
            if cart_product:
                data['qty'] = cart_product.qty
                data['total_cost'] = cart_product.total_cost
        
        else:
            
            data.update({
                'in_cart': False,
                'in_wishlist': False
            })
            
        return data
    
    @property
    def formatted_price(self):
        
        return locale.currency(self.price, grouping=True)
        
    @property
    def formatted_discounted_price(self):
        
        return locale.currency(self.discounted_price, grouping=True)
        
    @property
    def is_on_sale(self):
        
        return False
        
    @property
    def total_rating(self):
        
        return 3
    
    @property
    def in_stock(self):
        
        return bool(self.available_qty)
        
    @property
    def in_stock_label(self):
        
        if self.in_stock:
            return 'In stock'
            
        return 'Sold out'
        
class BaseCartProduct(object):
    
    @property
    def total_cost(self):
        
        return self.qty * self.product.price
    
    def as_dict(self, **kwargs):
        
        data = {
            'id': self.id,
            'qty': self.qty
        }
        
        if kwargs.get('include_product', False):
            
            product = self.product.as_dict(**kwargs)
            data.update(product)
            
        return data
