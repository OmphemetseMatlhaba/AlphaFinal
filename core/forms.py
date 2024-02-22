from django import forms
from .models import CropPrediction

class CropPredictionForm(forms.ModelForm):
    class Meta:
        model = CropPrediction
        fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'pH', 'rainfall']