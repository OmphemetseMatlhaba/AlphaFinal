from django.db import models

# Create your models here.
# sos/models.py

from django.db import models
from accounts.models import BasicAccount

class SOSCall(models.Model):
    user = models.ForeignKey(BasicAccount, on_delete=models.CASCADE, related_name='emergency_contacts', default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    additional_info = models.TextField(blank=True, null=True)
