from django.db import models
from item.models import Item
from accounts.models import BasicAccount


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount= models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ManyToManyField(BasicAccount, related_name='orders')
    
    
    class Meta:
        ordering = ['-created_at',]
        
        def __str__(self):
            return self.first_name
        
        
class OrderItem(models.Model):
    order= models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
    item=models.ForeignKey(Item, related_name='items', on_delete=models.CASCADE)
    user = models.ForeignKey(BasicAccount, related_name='items', on_delete=models.CASCADE)
    user_paid=models.BooleanField(default=False)
    price= models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    
        
    def __str__(self):
            return '%s' % self.id
        
    def total_price(self):
        return self.price * self.quantity
    
    


# Create your models here.
