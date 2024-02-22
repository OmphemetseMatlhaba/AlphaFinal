from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.shortcuts import redirect
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.contrib import messages
from django.db.models import Sum

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, password):
        if not username: 
            username = email.split('@')[0]
        
        if not email:
            raise ValueError('Please enter an email address')
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, username, password):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = self.normalize_email(email),
            password = password
        )
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
    
class BasicAccount(AbstractBaseUser):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255, unique = True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    profile_complete = models.BooleanField(default = False)
    profile_public = models.BooleanField(default = False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
    def get_total_upvotes(self):
        return self.farmer.aggregate(Sum('upvotes'))['upvotes__sum'] or 0
    
    def get_total_comments(self):
        return self.farmer_comment.count()
    
    def get_total_posts(self):
        return self.farmer.count()
    
    def get_total_subcomments(self):
        return self.farmer_sub_comment.count()
    
    def get_total_downvotes(self):
        return self.farmer.aggregate(Sum('downvotes'))['downvotes__sum'] or 0
    

class AdditionalInfo(models.Model):
    user = models.OneToOneField(BasicAccount, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to = 'profile_pictures', default='profile_pictures\default_profile.png')
    phone_number = models.CharField(max_length = 10, null=True, blank=True)
    home_address = models.CharField(max_length = 255, null=True, blank=True)
    suburb = models.CharField(max_length = 255, null=True, blank=True)
    city = models.CharField(max_length = 255, null=True, blank=True)
    province_choices = {
        ('Northern Cape', 'Northern Cape'),
        ('North West', 'North West'),
        ('Western Cape', 'Western Cape'),
        ('Eastern Cape', 'Eastern Cape'),
        ('Gauteng', 'Gauteng'),
        ('Limpopo', 'Limpopo'),
        ('Mpumalanga', 'Mpumalanga'),
        ('Free State', 'Free State'),
        ('Kwa-Zulu Natal', 'Kwa-Zulu Natal'),
    }
    province = models.CharField(max_length=50, choices=province_choices, null=True, blank=True)
    postal_code = models.CharField(max_length = 255, null=True, blank=True)
    longitude = models.CharField(max_length = 10, null=True, blank=True) 
    latitude = models.CharField(max_length = 10, null=True, blank=True)

    def __str__(self):
        return self.user.email
    

class FarmInfo (models.Model):
    farmer = models.ForeignKey(BasicAccount, on_delete=models.CASCADE, related_name='farm_info')
    name = models.CharField(max_length = 255, blank = True, null = True)
    location = models.CharField(max_length = 255, blank = True, null = True)
    size = models.IntegerField(blank = True, null = True)
    industry_options = {
        ('Crop Farming', 'Crop Farming'),
        ('Herding', 'Herding'),
        ('Mixed', 'Mixed'),
    }
    industry = models.CharField(max_length=30 ,choices = industry_options, null=True, blank=True)
    farming_practice_choices = {
        ('Organic Farming', 'Organic Farming'),
        ('Conventional Farming', 'Conventional Farming'),
        ('Sustainable Farming', 'Sustainable Farming'),
        ('Regenarative Farming', 'Regenarative Farming'),
        ('Precision Farming', 'Precision Farming'),
        ('Permaculture', 'Permaculture'),
        ('No-Till Farming', 'No-Till Farming'),
        ('Hydroponics & Aquaponics', 'Hydroponics & Aquaponics'),
    }
    farming_practices = models.CharField(max_length=30, choices=farming_practice_choices)
    crops_grown = models.CharField(max_length=255, null=True, blank=True)
    livestock_grown = models.CharField(max_length=255,null=True, blank=True)
    farming_specialty = models.CharField(max_length=255,null=True, blank=True)
    expertise = models.ManyToManyField('Expertise')
    certification = models.CharField(max_length=255,null=True, blank=True)
    farming_experience = models.IntegerField(blank = True, null=True)
    longitude = models.CharField(max_length=10, blank = True, null=True)
    latitude = models.CharField(max_length=10, blank = True, null=True)
    info_filled = models.BooleanField(default = False)

    def __str__(self):
        return f"{ self.farmer.first_name } { self.farmer.last_name }'s farm : { self.name }"

class Expertise (models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
@receiver(user_signed_up)
def user_signed_up_(request, user, sociallogin = None, **kwargs):
    profile, created = AdditionalInfo.objects.get_or_create(user=user)
    
    if sociallogin:      
       if sociallogin.account.provider == 'google':
        user.is_active = True

        profile_picture_url = sociallogin.account.extra_data.get('picture')
            
        if profile_picture_url:
                image_filename = os.path.basename(profile_picture_url)
                image_path = 'profile_pictures/{}'.format(image_filename) 
                
                response = requests.get(profile_picture_url)
                if response.status_code == 200:
                    content = ContentFile(response.content)
                    default_storage.save(image_path, content)
                    user.profile_picture = image_path
    if sociallogin.account.provider == 'microsoft':
         user.is_active = True
    user.save()
    profile.save()

class Achievements(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='forum/badges')

    def __str__(self):
        return self.name + ' ' + self.description
    
