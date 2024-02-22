from email.message import EmailMessage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

from django.template.loader import render_to_string
from cart.cart import Cart
from .models import Order, OrderItem

def checkout(request, first_name, last_name, email, address, postal_code, place, phone, amount):
    order=Order.objects.create(first_name=first_name, last_name=last_name, email=email, address=address, postal_code=postal_code, place=place, phone=phone, paid_amount=amount)
    
    for product in Cart(request):
        OrderItem.odjects.create(order=order, item=product['item'],  user=product['item'].user, price=product['item'].price, quantity=product['quantity'])
        
        order.users.add(product['item'].user)
        
        return order
    

def notify_customer(request):
    if request.method == 'POST':
        message =request.POST.get('message')
        email = request.Post['message']
        email = request.POST['email']
        name = request.POST['name']
        send_mail(
            'contact Form',
            message, #message
            'setting.EMAIL_HOST_USER', 
            ['omphemetsematlhaba@gmail.com'],
            fail_silently=False,
            )
        return render(request, 'marketplace/index.html')
    

