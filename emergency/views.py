# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from .models import SOSCall
from accounts.models import BasicAccount

@login_required
def initiate_sos(request):
    # Create an SOS call record
    user = request.user
    
    message_body = f"Disaster Alert in! Assistance required. " \
                   f"Farmer: {user.first_name} {user.last_name}, Contact: {user.email}, ",


    # Send an SOS SMS using Twilio
    twilio_account_sid = 'AC31d34a819a0828f4bb058cee8d5e8f6c'
    twilio_auth_token = '76e24d32b43a491c3a6612d24bf14de9'
    twilio_phone_number = '+1234567890'
    user_phone_number = request.user.profile.phone_number  # Assuming user has a profile with a phone number

    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(
        body=message_body,
        from_='+12512202936',
        to='+27662887519'
    )

    return redirect('home')  # Redirect to home page or wherever you want

def disaster_send(request):
    if request.method == 'POST':
        selected_location = request.POST.get('selected_location', None)
        if selected_location is not None:
            send_sms(request, selected_location)
            return render(request, 'emergency/disaster.html', {'selected_location': selected_location})
        else:
            # Handle the case when selected_location is not available
            return render(request, 'disaster.html', {'error_message': 'No Location selected'})
    else:
        return render(request, 'emergency/disaster.html', {})

def send_sms(request, selected_location):
    user = request.user
     # Retrieve the Farmer instance based on the user
    
    message_body = f"Disaster Alert in {selected_location}! Assistance required. " \
                   f"Farmer: {user.first_name} {user.last_name}, Contact:, City:"

    account_sid = 'AC31d34a819a0828f4bb058cee8d5e8f6c'
    auth_token = '76e24d32b43a491c3a6612d24bf14de9'
    
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message_body,
        from_='+12512202936',  # Your Twilio number
        to='+27662887519'  # Recipient's phone number (you should replace this with the actual recipient number)
    )

    print(message.sid)
    return redirect('home')

def disaster(request):
    return render(request, 'emergency/disaster.html', {})