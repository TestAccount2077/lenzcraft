from django.apps import apps

import json


def get_available_products(user, **kwargs):
    
    Product = apps.get_model('main.Product')
    
    return json.dumps([
        product.as_dict(
            user,
            include_review_details=kwargs.get('is_detail_view', False) and kwargs.get('product_id') == product.id
        )
        for product in Product.objects.filter(
            published=True,
            **kwargs.get('filter_kwargs', {})
        )
    ])
