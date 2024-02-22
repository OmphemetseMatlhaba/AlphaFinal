from django.urls import path

from . import views 

app_name='chat'

urlpatterns =[
    path('chat/<int:item_pk>/', views.new_chat, name='chat'),
    path('inbox/', views.inbox, name='inbox'),
    path('<int:pk>/', views.chatDetail, name='chatDetail'),
    
   
    path('new_equipment_chat/<int:equipment_pk>/', views.new_equipment_chat, name='new_equipment_chat'),

    # URL for viewing details of a specific equipment chat
    path('equipment_chat_detail/<int:pk>/', views.equipment_chat_detail, name='equipment_chat_detail'),

    
]
  
