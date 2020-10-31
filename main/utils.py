from django.apps import apps

import json


def get_available_products(user, as_json=True, **kwargs):
    
    Product = apps.get_model('main.Product')
    
    products = [
        product.as_dict(
            user,
            include_review_details=kwargs.get('is_detail_view', False) and kwargs.get('product_id') == product.id
        )
        for product in Product.objects.filter(
            published=True,
            **kwargs.get('filter_kwargs', {})
        ).exclude(**kwargs.get('exclude_kwargs', {}))
    ]
    
    products.extend([
        product.as_dict(user=user, include_product=True, is_cart_product=True) for product in user.cart.cart_products.all()
    ])
    
    if as_json:
        products = json.dumps(products)
        
    return products
