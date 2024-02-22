from django import forms
from .models import ChatMessage, EquipmentChatMessage

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields= ('content',)
        widgets= {
            'content': forms.Textarea(attrs={'width':   '100% '}),
        }
     
class EquipmentChatMessageForm(forms.ModelForm):
    class Meta:
        model = EquipmentChatMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'width': '100%'}),
        }