import os
import re
from django.shortcuts import get_object_or_404, redirect, render
import requests
from accounts.forms import AdditionalInfoForm, BasicInfoForm, FarmInfoForm, RegistrationForm
from accounts.models import Achievements, AdditionalInfo, BasicAccount, FarmInfo
from django.contrib import messages, auth
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login

from forum.models import FarmerAchievement



# Create your views here.

def validate_name(name):
    pattern = r'^[a-zA-Z]+([- ]?[a-zA-Z]+)*$'
    return re.match(pattern, name)

def register(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            username = email.split('@')[0]

            existing_user = BasicAccount.objects.filter(email=email)
            if existing_user:
                messages.info(request, 'Account already exists')
                print('Account already exists')
                return redirect('register')

            if password != repeat_password:
                messages.error(request, "Password and confirmation do not match")
                return redirect('register')
            
            if validate_name(first_name) and validate_name(last_name):
                print("names are okay")
            else:
                messages.error(request, "Names are invalid. Please try again.")
                return redirect('register')
            
            user = BasicAccount.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()

            additional_info = AdditionalInfo.objects.create(user = user)
            additional_info.save()

            current_site = '127.0.0.1:8000'
            mail_subject = 'Account Activation'
            message = 'Hello and welcome. Thank you for registering with PinIT'
            html_content = render_to_string('mail/activation_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = 'html'
            send_email.body = html_content
            send_email.send()
            messages.success(request, "Registration successful. Verification email sent to " + user.email)
            print('Registration successful')
            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    
    return render(request, 'accounts/register.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = BasicAccount._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, BasicAccount.DoesNotExist) as e:
        print(f"Activation error: {e}")
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if user.is_active:
            messages.warning(request, "Account already activated. Please log in.")
        else:
            user.is_active = True
            user.save()
            authenticated_user = authenticate(request, email=user.email)
            auth.login(request, authenticated_user)
            messages.success(request, "Account activated successfully. Welcome!")
            return redirect('edit_profile')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link. Please check the link or contact support.')
        return redirect('register')
    
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                profile = BasicAccount.objects.get(email = request.user)
                if profile.profile_complete:
                    messages.success(request, f'Welcome back, { profile.first_name}')
                    return redirect('home')
                else:
                    messages.success(request, f'Welcome back, { profile.first_name}, Please complete your profile.')
                    return redirect('edit_profile')
            else:
                print('Authentication failed')
                messages.error(request, 'Invalid email or password')
        except BasicAccount.DoesNotExist:
            print('Authentication failed')
            messages.error(request, 'Invalid email or password')
    return render(request, 'accounts/login.html')

    
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout successful, come back later')
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if BasicAccount.objects.filter(email=email).exists():
            user = BasicAccount.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Password reset'

            message = render_to_string('mail/password_reset_email.html', {
                'user': user,
                'domain': current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email sent.')

            return redirect('login')
        else:
            messages.error(request, 'Account not found. perhaps register a new one?')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = BasicAccount._default_manager.get(pk=uid)
    except(TypeError, ValueError, BasicAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Now reset the password')
        return redirect ('reset_password')
    else:
        messages.error(request, 'This link does not exist')
        return redirect ('login')
    
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['newPass']
        confirmPassword = request.POST['reNewPass']

        if password == confirmPassword:
            uid = request.session.get('uid')
            user = BasicAccount.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect ('login')
        
        else:
            messages.error(request, 'Passwords do not match')
            return redirect ('reset_password')
    else:
        return render(request, 'accounts/reset_password.html')

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        profile = get_object_or_404(AdditionalInfo, user=request.user)
        basic_info = BasicInfoForm(request.POST, instance=request.user)
        additional_info = AdditionalInfoForm(request.POST, request.FILES, instance=profile)

        if basic_info.is_valid() and additional_info.is_valid():
            basic_info.save()
            additional_info.save()
            user_account = BasicAccount.objects.get(email=request.user)
            user_account.profile_complete = True
            user_account.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('edit_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        profile = get_object_or_404(AdditionalInfo, user=request.user)
        basic_info = BasicInfoForm(instance=request.user)
        additional_info = AdditionalInfoForm(instance=profile)

    context = {
        'basic_info': basic_info,
        'additional_info': additional_info,
        'profile_picture': profile.profile_picture if request.user.is_authenticated else None,
    }

    return render(request, 'user_dashboard/edit_profile.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        retype_new_password = request.POST['retype_new_password']

        user = BasicAccount.objects.get(username__exact = request.user.username)

        if new_password == retype_new_password:
            check = user.check_password(current_password)
            if check:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully, please log in using the new password')
                return redirect('change_password')
            else:
                messages.error(request, 'Wrong password entered')
                return redirect('change_password')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('change_password')
        
    context = {}

    if request.user.is_authenticated:
        profile = AdditionalInfo.objects.get(user = request.user )
        context['profile_picture'] = profile.profile_picture
    return render(request, 'user_dashboard/change_password.html', context)

@login_required(login_url='login')
def farm_info (request):
    farmer, created = FarmInfo.objects.get_or_create(farmer = request.user)
    
    if request.method == 'POST':
        farm_info = FarmInfoForm(request.POST, instance = farmer)
        if farm_info.is_valid():
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']
            form = farm_info.save(commit=False)
            form.latitude = latitude
            form.longitude = longitude
            form.info_filled = True
            form.save()        
            messages.success(request, 'Farm information saved')
            return redirect('farm_info')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('farm_info')
    else: 
        farm_info = FarmInfoForm(instance = farmer)
    
    current_lat = farmer.latitude
    current_lon = farmer.longitude
    
    context = {
        'farm_info': farm_info,
        'farmer': farmer,
        'current_lat': current_lat,
        'current_lon': current_lon, 
    }

    if request.user.is_authenticated:
        profile = AdditionalInfo.objects.get(user = request.user )
        context['profile_picture'] = profile.profile_picture

    return render(request, 'user_dashboard/farm_info.html', context)

def user_analytics(request):
    user = request.user

    possible_achievements = Achievements.objects.all()
    user_achievements = FarmerAchievement.objects.filter(farmer = user.id)
    context = {
        'possible_achievements': possible_achievements,
        'user_achievements': user_achievements,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'user_dashboard/user_analytics.html', context)