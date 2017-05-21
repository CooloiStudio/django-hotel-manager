# coding: utf-8

from django.db import models

from RoomManage.models import Room

# Create your models here.


class Item(models.Model):
    name = models.CharField(u'物品名', max_length=100, unique=True)
    amount = models.IntegerField(u'数量')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'物资'
        verbose_name_plural = verbose_name


class RoomItem(models.Model):
    room = models.ForeignKey(Room, verbose_name=u'客房号')
    item_name = models.ForeignKey(Item, to_field='name', verbose_name=u'物品名')
    amount = models.IntegerField(u'数量', default=0)
    price = models.DecimalField(u'价格', max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return 'Room number : ' + str(self.room.room_num)

    class Meta:
        verbose_name = u'各房间物资'
        verbose_name_plural = verbose_name

