import locale

locale.setlocale(locale.LC_ALL, '')


class BaseProduct(object):
    
    @property
    def brand_name(self):
        return getattr(self.brand, 'name', '')
        
    @property
    def frame_type_name(self):
        return getattr(self.frame_type, 'name', '')
        
    @property
    def type_name(self):
        return getattr(self.type, 'name', '')
        
    @property
    def color_names(self):
        
        return [color.name for color in self.colors.all()]
        
    @property
    def split_list_description(self):
        
        return self.list_description.split('\n') if self.list_description else []
        
    def as_dict(self, user=None, **kwargs):
        
        price = self.formatted_price
        discounted_price = self.formatted_discounted_price
        
        DEFAULT_IMAGE_URL = 'https://lenzcraft.herokuapp.com/static/img/212X200/img2.jpg'
        
        data = {
            'name': self.name,
            'type': self.type_name,
            'category': self.get_category_display(),
            'model_number': self.model_number,
            'image_url': self.main_image.url if self.main_image else self.image_url or DEFAULT_IMAGE_URL,
            'detail_images': [image.as_dict() for image in self.detail_images.all()],
            'price': self.price,
            'discounted_price': self.discounted_price,
            'billing_price': self.discounted_price if self.discounted_price else self.price,
            'formatted_price': discounted_price if self.discounted_price else price,
            'formatted_discounted_price': price if self.discounted_price else discounted_price,
            
            'published': self.published,
            'is_featured': self.is_featured,
            'is_top_rated': self.is_top_rated,
            
            'brand': self.brand_name,
            'colors': self.color_names,
            'frame_type': self.frame_type_name,
            
            'created_timestamp': self.created.timestamp(),
            'total_rating': self.total_rating,
            'reviews': [review.as_dict() for review in self.reviews.all()],
            'url': f'/products/{ self.id }/',
            'available_qty': self.available_qty,
            'in_stock': self.in_stock,
            'in_stock_label': self.in_stock_label,
            
            'list_description': self.list_description,
            'split_list_description': self.split_list_description,
            'detail_description': self.detail_description
        }
        
        keyword = 'product_id' if kwargs.get('as_extention', False) else 'id'
        data[keyword] = self.id
            
        if user and user.is_authenticated:

            data.update({
                'in_cart': user.cart.cart_products.filter(product=self).exists(),
                'in_wishlist': user.wishlist.products.filter(id=self.id).exists()
            })
        
        else:
            
            data.update({
                'in_cart': False,
                'in_wishlist': False
            })
            
        if kwargs.get('include_review_details', False):
            
            review_count = self.reviews.count()
            
            for x in range(1, 6):
                
                rated_count = self.reviews.filter(rating=x).count()
                
                data[f'rated_{ x }'] = {
                    'count': rated_count,
                    'percentage': round((rated_count / (review_count or 1)) * 100, 2)
                }
            
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
        
        reviews = self.reviews.all()
        
        # perfect_rating = (len(reviews) or 1) * 5
        
        return round(sum(review.rating for review in reviews) / (len(reviews) or 1), 2)
    
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
    
    @property
    def name_with_color(self):
        
        name = self.product.name
        
        if self.color:
            return f'{ name } ({ self.color.name })'
        
        return name
        
    def as_dict(self, **kwargs):
        
        data = {
            'id': self.id,
            'qty': self.qty,
            'name_with_color': self.name_with_color,
            'is_cart_product': kwargs.get('is_cart_product', False)
        }
        
        if kwargs.get('include_product', False):
            
            data['cart_product_id'] = self.id
            product = self.product.as_dict(**kwargs)
            data.update(product)
            
        return data


class BaseProductReview(object):
    
    def as_dict(self):
        
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'content': self.content,
            'rating': self.rating,
            'timestamp': self.formatted_created
        }
        
    @property
    def formatted_created(self):
        
        return self.created.strftime('%B %d, %Y')


class BaseImage(object):
    
    def as_dict(self):
        
        return {
            'id': self.id,
            'name': getattr(self.image, 'name', 'Unnamed image'),
            'url': getattr(self.image, 'url', '#')
        }
