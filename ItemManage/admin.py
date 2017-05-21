# coding: utf-8

from django.contrib import admin

from .models import Item, RoomItem
# Register your models here.


class InfoItem(admin.ModelAdmin):
    list_display = (
        'name',
        'amount',
    )

admin.site.register(Item, InfoItem)


class InfoRoomItem(admin.ModelAdmin):
    list_display = (
        'amount',
        'price',
    )

admin.site.register(RoomItem, InfoRoomItem)
