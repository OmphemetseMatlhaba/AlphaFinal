from datetime import datetime, timezone
from django.shortcuts import redirect, render
from noticeboard.forms import CreateEventForm
from noticeboard.models import EventAttending, EventCategory, Event, EventInterested
from django.contrib import messages
import traceback
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def main(request):
    categories = EventCategory.objects.all()
    unique_provinces = Event.objects.values_list('province', flat=True).distinct()
    events_per_page = 6
    today = datetime.now(timezone.utc)
    events = Event.objects.filter(past_event = False).order_by('created_at')
    sort = request.GET.get('sort', '')
    if sort:
        events = Event.objects.filter(past_event = False).order_by(sort)
    for event in events:
        if today > event.date_time:
            event.past_event = True
        else:
            event.past_event = False
        event.save()
    paginator = Paginator(events, events_per_page)
    page = request.GET.get('page', 1)
    highest_reactions_event = Event.objects.annotate(total_reactions=Sum(F('interested') + F('attending'))).order_by('-total_reactions').first()
    
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)


    context = {
        'categories': categories,
        'events': events,
        'most_popular': highest_reactions_event,
        'sort': sort,
        'unique_provinces': unique_provinces,
    }

    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture

    return render(request, 'noticeboard/main.html', context)

def create_event(request):
    categories = EventCategory.objects.all()
    farmer = request.user

    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES)
        date_time_str = request.POST.get('date_time')
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
        formatted_date_time = date_time_obj.strftime('%Y-%m-%d %H:%M:00')
        print(formatted_date_time)

        if form.is_valid():
            try:
                post_form = form.save(commit=False)
                post_form.farmer = farmer
                post_form.date_time = formatted_date_time
                post_form.interested = 0
                post_form.attending = 0
                post_form.save()
                print(post_form)
                messages.success(request, 'Event created successfully')
                return redirect('noticeboard')
            except Exception as e:
                print(f"Error creating event: {e}")
                traceback.print_exc()
                messages.error(request, f'Error creating event: {e}')
                return redirect('create_event')
        else:
            errors = form.errors
            print(errors)
            messages.error(request, f'Form is not valid. Errors: {errors}')
            return redirect('create_event')

    else:
        form = CreateEventForm()

    context = {
        'form': form,
        'categories': categories,
    }

    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture

    return render(request, 'noticeboard/create_event.html', context)

def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    timestamp = int(event.date_time.timestamp())
    user_interested = None
    user_attending = None
    if request.user.is_authenticated:
        user_interested = EventInterested.objects.filter(user=request.user, event=event).exists()
        user_attending = EventAttending.objects.filter(user=request.user, event=event).exists()

    context = {
        'event': event,
        'timestamp': timestamp,
        'user_interested': user_interested,
        'user_attending': user_attending,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture

    return render(request, 'noticeboard/event_details.html', context)

def interested(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user

    event_interested = EventInterested.objects.filter(user=user, event=event)
    event_attending = EventAttending.objects.filter(user=user, event=event)

    if event_interested.exists():
        event_interested.delete()
        event.interested -= 1
        if event.interested < 0:
            event.interested = 0
    else:
        EventInterested.objects.create(user=user, event=event)
        event.interested += 1
        if event_attending.exists():
            event_attending.delete()
            event.attending -= 1
            if event.attending < 0: 
                event.attending = 0
            
    
    event.save()
    return redirect('event_details', event_id=event_id)

def attending(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user

    event_attending = EventAttending.objects.filter(user=user, event=event)
    event_interested = EventInterested.objects.filter(user=user, event=event)

    if event_attending.exists():
        event_interested.delete()
        event.attending -= 1
        if event.attending < 0:
            event.attending = 0
    else:
        EventAttending.objects.create(user=user, event=event)
        event.attending += 1
        if event_interested.exists():
            event_interested.delete()
            event.interested -= 1
            if event.interested < 0:
                event.attending = 0

    event.save()
    return redirect('event_details', event_id=event_id)

def filter_category(request, category_id=None):
    categories = EventCategory.objects.all()
    unique_provinces = Event.objects.values_list('province', flat=True).distinct()
    events = Event.objects.filter(past_event = False, event_category_id=category_id).order_by('date_time')
    events_per_page = 6
    paginator = Paginator(events, events_per_page)
    page = request.GET.get('page', 1)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    selected_category = EventCategory.objects.get(id=category_id)
    selected_category_id = int(category_id)
    context = {
        'events': events,
        'categories': categories,
        'selected_category': selected_category,
        'unique_provinces': unique_provinces,
        'selected_category_id': selected_category_id
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'noticeboard/view_category.html', context)


def filter_location(request, location):
    categories = EventCategory.objects.all()
    unique_provinces = Event.objects.values_list('province', flat=True).distinct()
    events = Event.objects.filter(province=location, past_event=False).order_by('date_time')
    chosen_location = str(location)
    context = {
        'categories': categories,
        'unique_provinces': unique_provinces,
        'events': events,
        'location': location,
        'chosen_location': chosen_location,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'noticeboard/view_location.html', context)

@login_required(login_url='login')
def user_events(request):
    categories = EventCategory.objects.all()
    unique_provinces = Event.objects.values_list('province', flat=True).distinct()
    events = Event.objects.filter(farmer=request.user)
    context = {
        'categories': categories,
        'unique_provinces': unique_provinces,
        'events': events,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'noticeboard/user_events.html', context)

def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    categories = EventCategory.objects.all()
    unique_provinces = Event.objects.values_list('province', flat=True).distinct()

    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            edit_form = form.save(commit=False)
            updated_date = request.POST.get('date_time', None)
            if updated_date is not None:
                edit_form.date_time = updated_date
            edit_form.save()
            messages.success(request, 'Event edited successfully')
            return redirect('event_details', event_id=event_id)
        else:
            messages.error(request, 'Something went wrong')
            return redirect('edit_event', event_id=event_id)
    else:
        form = CreateEventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'categories': categories,
        'unique_provinces': unique_provinces,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'noticeboard/edit_event.html', context)

def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect('user_events')

