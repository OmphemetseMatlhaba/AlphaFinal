from django.urls import path
from . import views


app_name = 'item'

urlpatterns = [
    path('items/', views.items, name='items'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    
    path('add_equipment_request/', views.add_equipment_request, name='add_equipment_request'),
    path('request_success/', views.request_success, name='request_success'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),
    path('accept_request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('equipment-listing/', views.equipment_listing, name='equipment_listing'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),

    
   
    path('admin/hire-requests/', views.view_hire_requests, name='view_hire_requests'),
    path('admin/hire-requests/accept/<int:hire_request_id>/', views.accept_hire_request, name='accept_hire_request'),
    path('admin/hire-requests/reject/<int:hire_request_id>/', views.reject_hire_request, name='reject_hire_request'),
    path('items/hire-requests/', views.hire_requests, name='hire_requests'),

    
    path('items/make_hire_request/<int:hire_request_id>/', views.make_hire_request, name='make_hire_request'),


    path('checkout/<int:hire_request_id>/', views.checkout, name='checkout'),
    
      
]
