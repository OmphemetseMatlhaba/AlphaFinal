from django.urls import path
from .views import faq, get_faq_details

app_name='marketplace'

urlpatterns = [
    # other patterns
    path('faq/', faq, name='faq'),
    path('get_faq_details/<int:faq_id>/', get_faq_details, name='get_faq_details'),

    # other patterns
]
    