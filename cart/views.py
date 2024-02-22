# views.py
from django.conf import settings
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CartItem
from item.models import Item
from .forms import CheckoutForm 
from order.utilities import checkout, notify_customer
from order.models import Order, OrderItem

from cart.models import models




def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user = request.user

    # Check if the item is already in the user's cart
    cart_item, created = CartItem.objects.get_or_create(user=user, item=item)

    # If the item is already in the cart, increase the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{item.name} added to your cart.")
    return redirect('view_cart')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.item.name} removed from your cart.")
    return redirect('view_cart')

def update_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()
        messages.success(request, f"Quantity updated for {cart_item.item.name}.")

    return redirect('view_cart')



def clear_cart(request):
    if request.method == 'POST':
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, "Your cart has been cleared.")
    
    return redirect('view_cart')

from django.db.models import Sum

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            
            stripe_token = form.cleaned_data['stripe_token']
            
            # Get the cart items
            cart_items = CartItem.objects.filter(user=request.user)

            # Calculate the total cost of the cart items in cents
            total_cost_cents = max(int(sum(item.total_price() for item in cart_items) * 100), 1000)

            try:
                # Create a charge using the Stripe API
                charge = stripe.Charge.create(
                    amount=total_cost_cents,
                    currency='ZAR',
                    description='Charge from YourAppName',
                    source=stripe_token
                )

                # Process the order and clear the cart
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                postal_code = form.cleaned_data['postal_code']
                place = form.cleaned_data['place']
                phone = form.cleaned_data['phone']

                order = checkout(request, first_name, last_name, email, address, postal_code, place, phone, total_cost_cents / 100)

                # Clear the cart items for the current user
                cart_items.delete()

                # Notify the customer
                #notify_customer(order)

                # Redirect to a success page
                return redirect('success')
            
            except stripe.error.CardError as e:
                # Display error to the user
                messages.error(request, f'Card Error: {e.error.message}')
                return redirect('payment')

            except Exception as e:
                # Handle other exceptions
                messages.error(request, f'There was an error processing your payment: {e}')
                return redirect('success')
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'stripe_pub_key': settings.STRIPE_PUB_KEY,
    }

    return render(request, 'marketplace/checkout.html', context)





def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            # Create a new order
            order = Order.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                place=form.cleaned_data['place'],
                paid_amount=total_price,  # You need to define total_price in your view
                # Assuming you want to associate the order with the current user
                # If not, adjust this accordingly
                user=request.user,
            )

            # Add each item from the cart to the order
            for cart_item in cart_items:
                order.items.add(cart_item.item, through_defaults={'quantity': cart_item.quantity})

            # Clear the cart (optional, depending on your business logic)
            cart_items.delete()

            # Redirect to a confirmation page or any other page as needed
            return redirect('order_confirmation')
    else:
        form = CheckoutForm()

    # Calculate the total price for each cart item
    total_price_dict = cart_items.aggregate(total_price=models.Sum(models.F('quantity') * models.F('item__price')))
    total_price = total_price_dict.get('total_price', 0)  # Get the total price from the dictionary

    context = {
        'form': form,
        'stripe_pub_key': settings.STRIPE_PUB_KEY,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'marketplace/view_cart.html', context)


def success_view(request):

    user = request.user
    cart_items = CartItem.objects.filter(user=request.user)

    context = {
        'user': user,
        
        'cart_items': cart_items,
    }


    return render(request , 'marketplace/success.html', context)

