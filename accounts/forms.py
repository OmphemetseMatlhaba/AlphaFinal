from urllib import request
from django import forms
from accounts.models import BasicAccount, AdditionalInfo, Expertise, FarmInfo
from django.contrib import messages
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control ', 'id': 'email', 'name': 'email'}), label='Email', required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = BasicAccount
        fields = ('first_name', 'last_name', 'email', 'password', 'repeat_password' , 'profile_public')

        def clean_email(self):
            email = self.cleaned_data.get('email')
            instance = getattr(self, 'instance', None)

            if instance and instance.pk is not None and BasicAccount.objects.filter(email=email).exclude(pk=instance.pk).exists():
                raise ValidationError(f'Email {email} is already in use')

            return email

class BasicInfoForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',}), disabled=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    profile_public = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'type': 'checkbox'}), required=False)
    class Meta:
        model = BasicAccount
        fields = ('email', 'first_name', 'last_name', 'profile_public')
        
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise ValidationError('First name should only contain alphabetic characters')
        return first_name
            
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise ValidationError('Last name should only contain alphabetic characters')
        return last_name

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.errors.get('first_name'):
            self.fields['first_name'].widget.attrs.update({'class': 'form-control is-invalid'})
        
        if self.errors.get('last_name'):
            self.fields['last_name'].widget.attrs.update({'class': 'form-control is-invalid'})


class AdditionalInfoForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
    home_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
    suburb = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
    province = forms.ChoiceField(choices=AdditionalInfo.province_choices ,widget=forms.Select(attrs={'class': 'form-control custom-select', 'style': 'height: 58px; background-color: white;'}), required = True)
    postal_code = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 9999}), required = True)

    class Meta:
        model = AdditionalInfo
        fields = ('profile_picture', 'phone_number', 'home_address', 'suburb', 'city', 'province', 'postal_code')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.errors.get('phone_number'):
            self.fields['phone_number'].widget.attrs.update({'class': 'form-control is-invalid'})
        
        if self.errors.get('profile_picture'):
            self.fields['phone_number'].widget.attrs.update({'class': 'form-control is-invalid'})
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if any(char.isalpha() for char in phone_number):
            raise ValidationError("Phone number should not contain alphabets.")
        
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValidationError("Phone number should be 10 digits long and should not contain alphabets.")
        return phone_number
    
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')

        if profile_picture:
            try:
                img = get_image_dimensions(profile_picture)
            except Exception as e:
                raise ValidationError("File is not a valid image.")

            max_size = 3 * 1024 * 1024 
            if profile_picture.size > max_size:
                raise ValidationError(f"File size must be no more than {max_size / (1024 * 1024)} MB.")

        return profile_picture
    
class FarmInfoForm(forms.ModelForm):
    
    class Meta:
        model = FarmInfo
        fields = ('name', 'location', 'size', 'industry', 'farming_practices', 'farming_experience', 'farming_specialty', 'crops_grown', 'livestock_grown', 'certification') 

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'location': forms.TextInput(attrs={'class': 'form-control', 'id': 'address-input', 'name': 'address-input'}),
                'size': forms.NumberInput(attrs={'class': 'form-control'}),
                'industry': forms.Select(attrs={'class': 'form-control bg-white', 'style': 'height: 58px;'}),
                'farming_practices': forms.Select(attrs={'class': 'form-control bg-white', 'style': 'height: 58px;'}),
                'farming_experience': forms.NumberInput(attrs={'class': 'form-control'}),
                'crops_grown': forms.TextInput(attrs={'class': 'form-control'}),
                'livestock_grown': forms.TextInput(attrs={'class': 'form-control'}),
                'certification': forms.TextInput(attrs={'class': 'form-control'}),
            }

