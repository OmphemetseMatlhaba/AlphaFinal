from django.shortcuts import render
from accounts.models import AdditionalInfo

# Create your views here.
def home(request):
    

    context = {} 

    if request.user.is_authenticated:
        profile = AdditionalInfo.objects.get(user = request.user)
        context['profile_picture'] = profile.profile_picture
    else:
        profile = None
    return render(request, 'main/home.html', context)
