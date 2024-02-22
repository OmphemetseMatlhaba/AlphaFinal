from django.contrib import admin
from accounts.models import BasicAccount, AdditionalInfo, FarmInfo, Expertise, Achievements

# Register your models here.

admin.site.register(BasicAccount)
admin.site.register(AdditionalInfo)
admin.site.register(FarmInfo)
admin.site.register(Expertise)
admin.site.register(Achievements)
