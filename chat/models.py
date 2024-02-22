from django.db import models
from django.contrib.auth.models import User
from accounts.models import BasicAccount

from item.models import Item, Equipment
# Create your models here.
class Chat(models.Model):
    item = models.ForeignKey(Item, related_name='chat', on_delete=models.CASCADE)
    farmer=models.ManyToManyField(BasicAccount, related_name='chat')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering= ('-modified_at',)
        
class ChatMessage(models.Model):
    chat= models.ForeignKey(Chat,related_name='message', on_delete=models.CASCADE)
    content = models.TextField()
    created_at= models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(BasicAccount, related_name='created_messages', on_delete=models.CASCADE)
    
  

class EquipmentChat(models.Model):
    equipment = models.ForeignKey(Equipment, related_name='equipment_chat', on_delete=models.CASCADE)
    farmer = models.ManyToManyField(BasicAccount, related_name='equipment_chat')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)

class EquipmentChatMessage(models.Model):
    equipment_chat = models.ForeignKey(EquipmentChat, related_name='equipment_chat_message', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(BasicAccount, related_name='created_equipment_messages', on_delete=models.CASCADE)
