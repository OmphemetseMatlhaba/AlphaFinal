from noticeboard import views
from django.urls import path

urlpatterns = [
    path('', views.main, name='noticeboard'),
    path('create_event/', views.create_event, name='create_event'),
    path('event_details/<int:event_id>', views.event_details, name='event_details'),
    path('user_interested/<int:event_id>', views.interested, name='user_interested'),
    path('user_attending/<int:event_id>', views.attending, name='user_attending'),
    path('view_category/<int:category_id>', views.filter_category, name='filter_category'),
    path('view_location/<str:location>', views.filter_location, name='filter_location'),
    path('view_user_events/', views.user_events, name='user_events'),
    path('edit_user_events/<int:event_id>', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete_event'),
]