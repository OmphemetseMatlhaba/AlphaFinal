# urls.py

from django.urls import path
from . import views 

urlpatterns = [
    path('initiate-sos/', views.initiate_sos, name='initiate_sos'),
    path('disaster_send/', views.disaster_send, name='disaster_send'),
    path('send-sms/', views.send_sms, name='send_sms'),
   
    # Other URL patterns...
]
