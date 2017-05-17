# coding: utf-8

from django.contrib import admin

from .models import Item, RoomItem
# Register your models here.

admin.site.register(Item)
admin.site.register(RoomItem)