from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status

from .utils import *
from .models import *
from .payment_processors import PaymentProcessor

from abstract.viewsets import CreateListRetrieveUpdateViewSet

from argparse import Namespace


class MainViewSet(CreateListRetrieveUpdateViewSet):
    
    queryset = Product.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    
    def home(self, request, *args, **kwargs):
        
        context = {
            'products': get_available_products(request.user)
        }
        
        return Response(context, template_name='home.html')
        
    def men_view(self, request, *args, **kwargs):
        
        context = {
            'products': get_available_products(request.user, filter_kwargs=dict(category='MN'))
        }
        
        return Response(context, template_name='men.html')
    
    def women_view(self, request, *args, **kwargs):
         
        context = {
            'products': get_available_products(request.user, filter_kwargs=dict(category='MN'))
        }
        
        return Response(context, template_name='women.html')
    
    def kids_view(self, request, *args, **kwargs):
    
        return Response({}, template_name='kids.html')
    
    def product_detail(self, request, pk, *args, **kwargs):
        
        product = Product.objects.filter(pk=pk).first()
        
        if not product:
            return Response({}, template='404.html')
        
        context = {
            'product': json.dumps(product.as_dict(user))
        }
        
        return Response(context, template_name='product-detail.html')
    
    def toggle_product_in_cart(self, request, *args, **kwargs):
        
        if request.is_ajax():
            
            user = request.user
            data = request.POST
            
            if not user.is_authenticated:
                return self._400('You must log in to add products to your cart. Log in and try again')
            
            product = Product.objects.filter(id=data['productId']).first()
            
            if not product:
                return JsonResponse({'error': 'Product not found'}, status=404)
            
            cart = user.cart
            qty = data.get('qty')
            
            if qty:
                qty = int(qty)
            
            cart_product = cart.cart_products.filter(product=product).first()
            
            if qty == 0 or (cart_product and qty is None):
                cart_product.delete()
                message = 'Product removed from cart'
                product = product.as_dict(user=user)
                
            else:
                print(qty)
                product = cart.cart_products.create(product=product, qty=qty or 1)
                message = 'Product added to cart'
                product = product.as_dict(user=user, include_product=True)
                
            return JsonResponse({
                'message': message,
                'product': product
            })
            
        return Response({}, template_name='index.html')
    
    def wishlist(self, request, *args, **kwargs):
        
        user = request.user
        
        products = []
        
        if user.is_authenticated:
            products = get_available_products(user, filter_kwargs=dict(wishlists=user.wishlist))
        
        context = {
            'products': products
        }
        
        return Response(context, template_name='wishlist.html')
    
    def cart(self, request, *args, **kwargs):
        
        user = request.user
        
        if not user.is_authenticated:
            return redirect('main:home')
        
        context = {
            'products': json.dumps([
                product.as_dict(user=user, include_product=True) for product in user.cart.cart_products.all()
            ])
        }
        
        return Response(context, template_name='cart.html')
    
    def toggle_product_in_wishlist(self, request, *args, **kwargs):
        
        if request.is_ajax():
            
            user = request.user
            data = request.POST
            
            product = Product.objects.filter(id=data['productId']).first()
            
            if not user.is_authenticated:
                return self._400('You must log in to add products to your wishlist. Log in and try again')
            
            if not product:
                return JsonResponse({'error': 'Product not found'}, status=404)
            
            wishlist = user.wishlist
            
            if product in wishlist.products.all():
                wishlist.products.remove(product)
                message = 'Product removed from wishlist'
                
            else:
                wishlist.products.add(product)
                message = 'Product added to wishlist'
        
            return JsonResponse({'message': message})
    
    def checkout(self, request, *args, **kwargs):
        
        context = {}
        
        return Response(context, template_name='checkout.html')
        
    def place_order(self, request, *args, **kwargs):
        
        if request.is_ajax():
            
            user = request.user
            data = request.POST
            
            processor = PaymentProcessor.build('tracknpay')
            
            request_data = Namespace(
                request_data=dict(
                    amount=5.0,
                    currency='EGP',
                    description='',
                    name=user.full_name,
                    email=user.email,
                    phone='',
                    city='Alex',
                    country='Egypt'
                )
            )
            
            response, successful = processor.process_one_time_payment(request_data)
            
            print(response, successful)
            
            return JsonResponse({})
    
    def faq(self, request, *args, **kwargs):
    
        return Response({}, template_name='faq.html')
    
    def about_us(self, request, *args, **kwargs):
    
        return Response({}, template_name='about.html')
    
    def contact_us(self, request, *args, **kwargs):
    
        return Response({}, template_name='contact.html')
        
    
