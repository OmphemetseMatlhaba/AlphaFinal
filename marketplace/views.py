from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from item.models import Category, Item
from .models import FAQCard
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)[0:8]
    categories = Category.objects.all()
    
    
    
    return render(request, 'marketplace/index.html', {
        'categories': categories,
        'items': items,
    })
    
def faq(request):
   faq_cards = FAQCard.objects.all()
   
   return render(request, 'marketplace/faq.html', {'faq_cards': faq_cards})

def get_faq_details(request, faq_id):
    try:
        faq = get_object_or_404(FAQCard, id=faq_id)
        data = {
            'title': faq.title,
            'details': faq.details,
            # Add more fields as needed
        }
        return JsonResponse(data)
    except FAQCard.DoesNotExist:
        return JsonResponse({'error': 'FAQ not found'}, status=404)