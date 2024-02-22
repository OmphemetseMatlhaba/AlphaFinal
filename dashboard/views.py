from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
# Create your views here.
from item.models import Item
from order.models import Order

def index(request):
    # Fetch items created by the user
    items = Item.objects.filter(created_by=request.user)

    # Fetch orders associated with the user
    orders = Order.objects.filter(user=request.user)

    # Iterate through orders and calculate additional information
    for order in orders:
        order.user_amount = 0
        order.user_paid_amount = 0
        order.fully_paid = True

        for order_item in order.items.all():
            if order_item.user == request.user:
                if order_item.user_paid:
                    order.user_paid_amount += order_item.total_price()
                else:
                    order.user_amount += order_item.total_price()
                    order.fully_paid = False

    return render(request, 'dashboard/index.html', {
        'items': items,
        'orders': orders,
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

