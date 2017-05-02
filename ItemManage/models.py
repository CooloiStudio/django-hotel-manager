from django.db import models

from RoomManage.models import Room

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    amount = models.IntegerField(max_length=7)

    def __str__(self):
        return self.name


class RoomItem(models.Model):
    room = models.ForeignKey(Room)
    item_name = models.ForeignKey(Item, to_field='name')
    amount = models.IntegerField(max_length=3, default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return 'Room number : ' + str(self.room.room_num)

