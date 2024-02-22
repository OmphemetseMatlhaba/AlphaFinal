from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class CropPrediction(models.Model):
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    pH = models.FloatField()
    rainfall = models.FloatField()
    predicted_crop = models.CharField(max_length=255, blank=True, null=True)
