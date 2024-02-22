from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField 
from accounts.models import BasicAccount

# Create your models here.

class EventCategory(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name = ('Event Category')
        verbose_name_plural = ('Event Categories')

    def __str__(self):
        return self.name 

class Event(models.Model):
    farmer = models.ForeignKey(BasicAccount, on_delete=models.CASCADE, related_name='event')
    name = models.CharField(max_length = 255, null = False, blank = False)
    date_time = models.DateTimeField(max_length = 255, null = False, blank = False)
    location = models.CharField(max_length = 255, null = False, blank = False)
    province = models.CharField(max_length = 255)
    event_category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    interested = models.IntegerField(default = 0)
    attending = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    description = RichTextUploadingField()
    past_event = models.BooleanField(default=False)
    image_cover = models.ImageField(upload_to='noticeboard/images', null=False, blank = False)

    def __str__(self):
        return self.name 
    
class EventInterested(models.Model):
    user = models.ForeignKey(BasicAccount, null=True, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
    
    def __str__(self):
        return f"{self.user.first_name} interested in {self.event.name}"
class EventAttending(models.Model):
    user = models.ForeignKey(BasicAccount, null=True, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'event')
    
    def __str__(self):
        return f"{self.user.first_name} attending {self.event.name}"
