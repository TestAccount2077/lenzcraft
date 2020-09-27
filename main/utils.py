from django.apps import apps

import json


def get_available_products(user, **kwargs):
    
    Product = apps.get_model('main.Product')
    
    return json.dumps([
        product.as_dict(user) for product in Product.objects.filter(published=True, **kwargs.get('filter_kwargs', {}))
    ])
