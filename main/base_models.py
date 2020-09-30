

class BaseProduct(object):
    
    def as_dict(self, user=None):
        
        data = {
            'id': self.id,
            'name': self.name,
            'type': self.get_type_display(),
            'category': self.get_category_display(),
            'model_number': self.model_number,
            'image_url': self.image_url,
            'price': self.price,
            'formatted_price': self.formatted_price,
            'published': self.published,
            'is_featured': True,
            'is_on_sale': True, # self.is_on_sale,
            
            'brand': self.brand,
            'color': self.color,
            'frame_type': self.get_frame_type_display(),
            
            'created_timestamp': self.created.timestamp(),
            'total_rating': self.total_rating,
            'reviews': [review.as_dict() for review in self.reviews.all()],
            'url': f'/products/{ self.id }/',
            'available_qty': self.available_qty,
            'in_stock': self.in_stock,
            'in_stock_label': self.in_stock_label,
            'qty': 0,
            'total_cost': 0
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
        
        return self.price
        
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
            
            product = self.product.as_dict()
            data.update(product)
            
        return data
