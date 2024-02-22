from django.contrib import admin
from noticeboard.models import EventCategory, Event
# Register your models here.

admin.site.register(EventCategory)
admin.site.register(Event)