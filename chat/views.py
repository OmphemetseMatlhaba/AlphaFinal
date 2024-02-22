from django.shortcuts import get_object_or_404, redirect, render
from item.models import Item
from .forms import ChatMessageForm,  EquipmentChatMessageForm
from .models import Chat, Equipment, EquipmentChat
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

@login_required
def new_chat(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')

    # Check if a chat already exists between the two users
    chat = Chat.objects.filter(item=item, farmer__in=[request.user, item.created_by])

    if chat.exists():
        # Redirect to the existing chat
        return redirect('chat:chatDetail', pk=chat.first().id)

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)

        if form.is_valid():
            # Create a new chat instance
            new_chat = Chat.objects.create(item=item)
            new_chat.farmer.add(request.user, item.created_by)

            chat_message = form.save(commit=False)
            chat_message.chat = new_chat
            chat_message.created_by = request.user
            chat_message.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = ChatMessageForm()

    return render(request, 'marketplace/chat.html', {'form': form})

@login_required
def inbox(request):
    chats = Chat.objects.filter(farmer__in=[request.user.id])
    equipment_chats = EquipmentChat.objects.filter(farmer=request.user).select_related('equipment')
    
    paginator = Paginator(equipment_chats, 10)  # Show 10 equipment chats per page
    page = request.GET.get('page')
    equipment_chats = paginator.get_page(page)

    
    return render(request, 'marketplace/inbox.html', {
        'chats': chats,
        'equipment_chats': equipment_chats
    })

@login_required
def chatDetail(request, pk):
    chat = get_object_or_404(Chat, farmer__in=[request.user.id], pk=pk)
    
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.chat = chat
            chat_message.created_by = request.user
            chat_message.save()
            
            return redirect('chat:chatDetail', pk=pk)
    else: 
        form = ChatMessageForm()

    return render(request, 'marketplace/chatDetail.html', {
        'chat': chat,
        'form': form
    })


@login_required
def new_equipment_chat(request, equipment_pk):
    equipment = get_object_or_404(Equipment, pk=equipment_pk)

    if equipment.created_by == request.user:
        return redirect('dashboard:index')

    # Check if a chat already exists between the two users
    equipment_chat = EquipmentChat.objects.filter(equipment=equipment,farmer__in=[request.user, equipment.created_by])

    if equipment_chat.exists():
        # Redirect to the existing chat
        return redirect('chat:equipment_chat_detail', pk=equipment_chat.first().id)

    if request.method == 'POST':
        form = EquipmentChatMessageForm(request.POST)

        if form.is_valid():
            # Create a new equipment chat instance
            new_equipment_chat = EquipmentChat.objects.create(equipment=equipment)
            new_equipment_chat.farmer.add(request.user, equipment.created_by)

            chat_message = form.save(commit=False)
            chat_message.equipment_chat = new_equipment_chat
            chat_message.created_by = request.user
            chat_message.save()

            return redirect('chat:equipment_chat_detail', pk=equipment_pk)
    else:
        form = EquipmentChatMessageForm()

    return render(request, 'marketplace/hire/equipment_chat.html', {'form': form})



@login_required
def equipment_chat_detail(request, pk):
    equipment_chat = get_object_or_404(EquipmentChat,farmer__in=[request.user.id], pk=pk)

    if request.method == 'POST':
        form = EquipmentChatMessageForm(request.POST)

        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.equipment_chat = equipment_chat
            chat_message.created_by = request.user
            chat_message.save()

            return redirect('chat:equipment_chat_detail', pk=pk)
    else:
        form = EquipmentChatMessageForm()

    return render(request, 'marketplace/hire/equipment_chat_detail.html', {
        'equipment_chat': equipment_chat,
        'form': form
    })