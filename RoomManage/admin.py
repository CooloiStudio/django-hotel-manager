# coding: utf-8

from django.contrib import admin
from .models import Room,Customs,Bills,Orders,Cost_Item
# Register your models here.

admin.site.register(Room)
admin.site.register(Customs)
admin.site.register(Bills)
admin.site.register(Orders)
admin.site.register(Cost_Item)