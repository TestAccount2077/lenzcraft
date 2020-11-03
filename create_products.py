import os
import django
import datetime
import random

os.environ['DJANGO_SETTINGS_MODULE'] = 'lenzcraft.settings'
django.setup()

from main.models import *


def create_products(count=100, delete_old=True):
    
    if delete_old:
        print('Deleted', Product.objects.all().delete()[0], 'old objects')
    
    TYPES = tuple(dict(Product.TYPES).values())
    FRAME_TYPES = tuple(dict(Product.FRAME_TYPES).values())
    CATEGORIES = Product.REVERSED_CATEGORIES
    
    HOST_URL = 'https://lenzcraft.herokuapp.com'
    
    get_image_url = lambda suffix: f'{ HOST_URL }/static/img/{ suffix }'
    
    IMAGE_URLS = (
        get_image_url('212X200/img1.jpg'),
        get_image_url('212X200/img2.jpg'),
        # get_image_url()
    )
    
    colors = ['Red', 'Blue', 'Brown', 'Pink', 'Black', 'White']
    chosen_colors = []
    
    for category, db_category in CATEGORIES.items():
        
        print(f'Creating products for { category } category...')
        
        for x in range(1, count + 1):
            if not colors:
                colors = chosen_colors.copy()
                chosen_colors = []
            
            color = random.choice(colors)
            colors.remove(color)
            
            if color not in chosen_colors:
                chosen_colors.append(color)
            
            if x % 10 == 1:
                brand_num = 1
                
            elif not x % 2:
                brand_num = 2
            
            elif not x % 3:
                brand_num = 3
            
            elif not x % 4:
                brand_num = 4
                    
            else:
                brand_num = 5
            
            product = Product.objects.create(
                name=f'{ category } product { x }',
                type=ProductType.objects.get_or_create(name=random.choice(TYPES))[0],
                category=db_category,
                frame_type=FrameType.objects.get_or_create(name=random.choice(FRAME_TYPES))[0],
                model_number=random.randint(100000, 999999),
                price=random.randrange(100, 3000, 50),
                brand=Brand.objects.get_or_create(name=f'{ category } brand { brand_num }')[0],
                image_url=random.choice(IMAGE_URLS),
                published=True
            )
            
            product.colors.add(Color.objects.get_or_create(name=color)[0])
            
            print(f'Created product named { product.name }')
    

if __name__ == '__main__':
    create_products()
