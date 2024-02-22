# marketplace/urls.py
from django.urls import path
from .utilities import notify_seller, notify_customer

urlpatterns = [
   
    path('notify-customer/<int:order_id>/', notify_customer, name='notify_customer'),
]
