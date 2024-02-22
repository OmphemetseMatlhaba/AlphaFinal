from django.contrib import admin

# Register your models here.
from . models import Chat, ChatMessage, EquipmentChat,EquipmentChatMessage

admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(EquipmentChat)
admin.site.register(EquipmentChatMessage)
