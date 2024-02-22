# models.py
from django.db import models

from accounts.models import BasicAccount
from item.models import Item

class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(BasicAccount, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} - {self.user.username}'s Cart"

    def total_price(self):
        return self.quantity * self.item.price