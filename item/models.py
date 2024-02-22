from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import BasicAccount
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name =models.CharField(max_length=255)
    
    class Meta:
        ordering= ('name'),
        verbose_name_plural = 'Categories'
        
    def __str__(self):
       return self.name
   
class Item(models.Model):
    category=models.ForeignKey(Category,related_name='items', on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    description = RichTextField(max_length=4000,null=True, blank=True) 
    price= models.FloatField()
    image=models.ImageField(upload_to= 'item_images', blank=True, null=True)
    is_sold=models.BooleanField(default=False)
    created_by = models.ForeignKey(BasicAccount, related_name='created_items', on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return self.name
   
class EquipmentCategory(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Equipment Categories'
        
    def __str__(self):
        return self.name





class Equipment(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='equipment_images/',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = RichTextField(null=True, blank=True) 
    available_for_hire = models.BooleanField(default=False)  # New field

    def __str__(self):
        return self.name


class EquipmentRequest(models.Model):
    user = models.ForeignKey(BasicAccount, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='equipment_requests/',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = RichTextField(max_length=4000,null=True, blank=True) 
    pdf_document = models.FileField(upload_to='equipment_requests/documents/',  blank=True, null=True)
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return self.name


class HireRequest(models.Model):
    
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    total_cost = models.FloatField(null=True, blank=True)
    total_days=models.IntegerField(null=True, blank=True)
    pdf_contract = models.FileField(upload_to='hire_requests/documents/', blank=True, null=True)
    pdf_idCopy= models.FileField(upload_to='hire_requests/documents/', blank=True, null=True)
    pdf_proof_of_residence = models.FileField(upload_to ='hire_request/documents/', blank=True, null=True)
    pdf_other= models.FileField(upload_to = 'hire_request/documents/', blank=True, null= True)
    farmer = models.ForeignKey(BasicAccount, on_delete=models.CASCADE, blank=True, null=True)
    request_date= models.DateTimeField(auto_now_add=True, null=True)


    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('INCOMPLETE', 'Incomplete'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='INCOMPLETE')

    def __str__(self):
        return f"Hire Request for {self.equipment.name}"
