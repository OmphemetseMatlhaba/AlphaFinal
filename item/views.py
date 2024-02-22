from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import item
from .models import Item, Category, EquipmentCategory, Equipment
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import EquipmentRequest, HireRequest
from .forms import EquipmentRequestForm, HireRequestForm, AddToCartForm, NewItemForm, EditItemForm
from django.contrib import messages
from cart.cart import Cart
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse
# Create your views here.

from django.shortcuts import get_object_or_404




def items(request):
    cart = Cart(request)
    
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        
        if form.is_valid():
          
                
                quantity = form.cleaned_data['quantity']
               
                cart.add(item_id=item.id, quantity=quantity, update_quantity=False)
                messages.success(request, 'The product was added successfully')
                return redirect('marketplace:items')
           
    
    else:
        form = AddToCartForm()
        
    if category_id:
        items = items.filter(category_id=category_id)
    
    if query: 
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'marketplace/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'form': form,
    })


def detail(request, pk):
    item= get_object_or_404(Item, pk=pk)
    related_items =Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    
    return render(request,'marketplace/detail.html',{
        'item':item,
        'related_items':related_items
        
})

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():   
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            return redirect('item:detail', pk=item.id)
    else: 
        form = NewItemForm()
    
    return render(request, 'marketplace/form.html', {'form': form})

    
@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
       
        if form.is_valid():   
            form.save()
            return redirect('item:detail', pk=item.id)
    else: 
        form = EditItemForm(instance=item)
    
    return render(request, 'marketplace/form.html', {
        'form': form,
    })

@login_required   
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')

    
    #Equipment
    from .forms import EquipmentRequestForm


def add_equipment_request(request):
    if request.method == 'POST':
        form = EquipmentRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item:request_success')
    else:
        form = EquipmentRequestForm()
    return render(request, 'marketplace/hire/equipment_request_form.html', {'form': form})

def request_success(request):
    # Add any additional context data here if needed
    context = {
        'message': 'Your equipment request has been successfully submitted.'
    }
    return render(request, 'marketplace/hire/request_success.html', context)

@login_required
def manage_requests(request):
    requests = EquipmentRequest.objects.all()
    return render(request, 'marketplace/admin/manage_requests.html', {'requests': requests})

@login_required
def accept_request(request, request_id):
    try:
        request_instance = EquipmentRequest.objects.get(pk=request_id)
    except EquipmentRequest.DoesNotExist:
        return HttpResponseNotFound("The requested equipment request does not exist.")

    request_instance.status = 'accepted'
    request_instance.save()
    
    # Create an instance of the Equipment model based on the request
    Equipment.objects.create(
        name=request_instance.name,
        category=request_instance.category,
        image=request_instance.image,
        price=request_instance.price,
        description=request_instance.description,
        available_for_hire=True
    )
    
    return redirect('item:manage_requests')

@login_required
def reject_request(request, request_id):
    try:
        request_instance = EquipmentRequest.objects.get(pk=request_id)
    except EquipmentRequest.DoesNotExist:
        return HttpResponseNotFound("The requested equipment request does not exist.")

    request_instance.status = 'rejected'
    request_instance.save()
    return redirect('item:manage_requests')

@login_required
def equipment_listing(request):
    available_equipment = Equipment.objects.filter(available_for_hire=True)
  
    return render(request, 'marketplace/hire/equipment_listing.html', {'available_equipment': available_equipment})
    
@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    user=request.user
    if request.method =="POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        total_cost = request.POST.get('total_cost')
        total_days = request.POST.get('total_days')
      


        hire_request = HireRequest( 
            start_date= start_date, 
            end_date= end_date, 
            total_cost= total_cost, 
            total_days=total_days,
            equipment=equipment,
            farmer=user,
            status="INCOMPLETE",
        )                         

        hire_request.save()

        return redirect('item:make_hire_request', hire_request_id=hire_request.id)


    context = {
        'equipment': equipment,
       
    }
    
    return render(request, 'marketplace/hire/equipment_detail.html', context)



@login_required
def make_hire_request(request, hire_request_id):

    hire_request = HireRequest.objects.get(id=hire_request_id)

    if request.method == 'POST':
        form= HireRequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_form = form.save(commit=False)
            request_form.status="PENDING"
            request_form.equipment=hire_request.equipment
            request_form.start_date=hire_request.start_date
            request_form.end_date=hire_request.end_date
            request_form.farmer=hire_request.farmer
            request_form.total_cost=hire_request.total_cost
            request_form.total_days=hire_request.total_days
            request_form.save()
            return redirect('item:request_success')

    else: 
        form= HireRequestForm()
    context ={
        'form': form,
        'hire_request': hire_request,


        
        }        


    return render(request, 'marketplace/hire/make_hire_request.html', context)


@login_required
def view_hire_requests(request,):
    # Redirect non-admin users

    hire_requests = HireRequest.objects.all()
    context = {'hire_requests': hire_requests}
    return render(request, 'marketplace/admin/view_hire_requests.html', context)

@login_required
def accept_hire_request(request, hire_request_id):
    if not request.user.is_staff:
        return redirect('home')  # Redirect non-admin users

    hire_request = get_object_or_404(HireRequest, id=hire_request_id)
    hire_request.status = 'ACCEPTED'
    hire_request.save()
    messages.success(request, 'Hire request accepted successfully.')
    return redirect('item:view_hire_requests')

@login_required
def reject_hire_request(request, hire_request_id):
    if not request.user.is_staff:
        return redirect('home')  # Redirect non-admin users

    hire_request = get_object_or_404(HireRequest, id=hire_request_id)
    hire_request.status = 'REJECTED'
    hire_request.save()
    messages.success(request, 'Hire request rejected successfully.')
    return redirect('item:view_hire_requests')

def hire_requests(request):
    if request.method == 'POST':
        # If a POST request is received, it means a delete action is requested
        hire_request_id = request.POST.get('hire_request_id')
        hire_request = get_object_or_404(HireRequest, id=hire_request_id)
        # Ensure that only the owner of the hire request can delete it
        if hire_request.farmer == request.user:
            hire_request.delete()
    # Retrieve hire requests for the current user after potential deletion
    hire_requests = HireRequest.objects.filter(farmer=request.user)
    context = {'hire_requests': hire_requests}
    return render(request, 'marketplace/hire/view_hire_requests.html', context)

def checkout(request, hire_request_id):
    # Retrieve the hire request object
    hire_request = get_object_or_404(HireRequest, id=hire_request_id)
    
    if request.method == 'POST':
        # Process checkout confirmation
        # For example, update the status of the hire request
        hire_request.status = 'Checked Out'
        hire_request.save()
        # Redirect to a success page or another relevant page
        return redirect('item:success')  # Replace 'your_success_url' with the actual URL name
    
    # Render the checkout page template
    context = {'hire_request': hire_request}
    return render(request, 'marketplace/hire/checkout.html', context)