# forms.py
from django import forms
from .models import Item, Equipment, HireRequest
from ckeditor.widgets import CKEditorWidget

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }) 
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (  'category', 'name', 'description', 'price', 'image', 'is_sold')
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
                }),
            
           'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })     
        }


        
class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()

    # forms.py
from django import forms
from .models import EquipmentRequest

class EquipmentRequestForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = EquipmentRequest
        fields = ['user', 'name', 'category', 'image', 'price', 'description', 'pdf_document']

from django import forms
from .models import HireRequest


class HireRequestForm(forms.ModelForm):
    class Meta:
        model = HireRequest
        fields = [ 'pdf_contract', 'pdf_idCopy', 'pdf_proof_of_residence', 'pdf_other']

