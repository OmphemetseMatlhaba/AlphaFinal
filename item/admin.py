from django.contrib import admin
from .models  import Category, Item,EquipmentCategory,Equipment,EquipmentRequest,HireRequest
# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(EquipmentCategory)
admin.site.register(Equipment)
admin.site.register(EquipmentRequest)
admin.site.register(HireRequest)



