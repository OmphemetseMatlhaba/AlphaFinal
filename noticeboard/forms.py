from noticeboard.models import Event, EventCategory
from django import forms

class CreateEventForm(forms.ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={'id': 'address_input', 'name': 'address_input'}))
    province = forms.CharField(widget=forms.TextInput(attrs={'id': 'province_input', 'name': 'province_input', 'readonly': 'readonly'}))
    class Meta:
        model = Event
        fields = ('name', 'description', 'location', 'province', 'event_category', 'image_cover')

    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-white'
    
    def clean_image_cover(self):
        image_cover = self.cleaned_data['image_cover']

        return image_cover