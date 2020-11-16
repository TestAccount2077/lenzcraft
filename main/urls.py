from django.conf.urls import url

from .views import *

app_name = 'main'


home = MainViewSet.as_view({
    'get': 'home'
})

men_view = MainViewSet.as_view({
    'get': 'men_view'
})

women_view = MainViewSet.as_view({
    'get': 'women_view'
})

kids_view = MainViewSet.as_view({
    'get': 'kids_view'
})

sunglasses_view = MainViewSet.as_view({
    'get': 'sunglasses_view'
})

product_detail = MainViewSet.as_view({
    'get': 'product_detail'
})

add_to_cart = MainViewSet.as_view({
    'post': 'add_to_cart'
})

wishlist = MainViewSet.as_view({
    'get': 'wishlist'
})

toggle_product_in_wishlist = MainViewSet.as_view({
    'post': 'toggle_product_in_wishlist'
})

toggle_product_in_cart = MainViewSet.as_view({
    'post': 'toggle_product_in_cart'
})

cart = MainViewSet.as_view({
    'get': 'cart'
})

checkout = MainViewSet.as_view({
    'get': 'checkout'
})

place_order = MainViewSet.as_view({
    'post': 'place_order'
})

faq = MainViewSet.as_view({
    'get': 'faq'
})

about_us = MainViewSet.as_view({
    'get': 'about_us'
})

contact_us = MainViewSet.as_view({
    'get': 'contact_us'
})

add_review = MainViewSet.as_view({
    'post': 'add_review'
})

virtual_try_view = MainViewSet.as_view({
    'get': 'virtual_try_view'
})

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^men/$', men_view, name='men'),
    url(r'^women/$', women_view, name='women'),
    url(r'^kids/$', kids_view),
    url(r'^sunglasses/$', sunglasses_view),
    url(r'^wishlist/$', wishlist),
    url(r'^checkout/$', checkout),
    url(r'^cart/$', cart),
    
    url(r'^about-us/$', about_us),
    url(r'^faq/$', faq),
    url(r'^contact-us/$', contact_us),
    
    url(r'^products/(?P<pk>\d+)/$', product_detail, name='product_detail'),
    url(r'^products/(?P<pk>\d+)/try/$', virtual_try_view, name='virtual_try'),
    
    url(r'ajax/add-to-cart/$', add_to_cart),
    url(r'ajax/toggle-product-in-wishlist/$', toggle_product_in_wishlist),
    url(r'ajax/toggle-product-in-cart/$', toggle_product_in_cart),
    url(r'ajax/place-order/$', place_order),
    
    url(r'^ajax/add-review/$', add_review),
]
