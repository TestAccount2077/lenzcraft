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
            'products': get_available_products(request.user)
        }
        
        return Response(context, template_name='men.html')
    
    def women_view(self, request, *args, **kwargs):
         
        context = {
            'products': get_available_products(request.user)
        }
        
        return Response(context, template_name='women.html')
    
    def kids_view(self, request, *args, **kwargs):
        
        context = {
           'products': get_available_products(request.user)
        }
       
        return Response(context, template_name='kids.html')
    
    def sunglasses_view(self, request, *args, **kwargs):
        
        context = {
           'products': get_available_products(request.user)
        }
        
        return Response(context, template_name='sunglasses.html')
    
    def product_detail(self, request, pk, *args, **kwargs):
        
        product = Product.objects.filter(pk=pk).first()
        
        if not product:
            return Response({}, template='404.html')
        
        context = {
            'productId': product.id,
            'productName': product.name,
            'products': get_available_products(request.user, is_detail_view=True, product_id=product.id),
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
            action = data['action']
            cart_product = cart.cart_products.filter(product=product).first()
            
            if action in ('increment', 'decrement'):
                qty = abs(int(data.get('qty', 1) or 1))
            
            get_update_message = lambda: f'Quantity updated successfully. You now have { cart_product.qty } x { cart_product.product.name } in your cart'
            
            if action == 'increment':
                if cart_product:
                    cart_product.qty += qty
                    cart_product.save()
                    message = get_update_message()
                    
                else:
                    cart_product = cart.cart_products.create(product=product, qty=qty)
                    message = 'Product added successfully'
                    
            elif action == 'decrement':
                if cart_product:
                    if cart_product.qty - qty <= 0:
                        return self._400('Value cannot be less than or equal to 0')
                        
                    cart_product.qty -= qty
                    cart_product.save()
                    message = get_update_message()
                
                else:
                    return self._404('Product not found in cart. Add to cart and try again')
                    
            elif action == 'toggle':
                if cart_product:
                    cart_product.delete()
                    message = 'Product removed successfully'
                    
                else:
                    cart_product = cart.cart_products.create(product=product, qty=1)
                    message = 'Product added successfully'
                
            elif action == 'remove':
                if cart_product:
                    cart_product.delete()
                    message = 'Product removed successfully'
                    
                else:
                    return self._404('Product not found in cart')
            
            return JsonResponse({
                'product': product.as_dict(user=user, include_product=True),
                'message': message
            })
            
        return Response({}, template_name='index.html')
    
    def wishlist(self, request, *args, **kwargs):
        
        user = request.user
        
        products = []
        
        if user.is_authenticated:
            products = get_available_products(user)
        
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
        
        context = {
           'products': get_available_products(request.user)
        }
        
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
        
        context = {
           'products': get_available_products(request.user)
        }
        
        return Response(context, template_name='faq.html')
    
    def about_us(self, request, *args, **kwargs):
        
        context = {
           'products': get_available_products(request.user)
        }
        
        return Response(context, template_name='about.html')
    
    def contact_us(self, request, *args, **kwargs):
        
        context = {
           'products': get_available_products(request.user)
        }
        
        return Response(context, template_name='contact.html')
        
    def add_review(self, request, *args, **kwargs):
        
        if request.is_ajax():
            
            user = request.user
            data = request.POST
            
            product = Product.objects.filter(id=data['productId']).first()
            
            if not product:
                return JsonResponse({'error': 'Product not found'}, status=404)
            
            product.reviews.create(
                name=data['name'],
                email=data['email'],
                content=data['content'],
                rating=int(data['rating'])
            )
            
            return JsonResponse({'product': product.as_dict(user, include_review_details=True)}, status=201)
