# urls.py
from django.urls import path
# urls.py
from django.urls import path
from .views import view_cart, success_view, checkout
from . import views



urlpatterns = [
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success_view, name='success'),
    
]