from django.db import models

# Create your models here.

class Room(models.Model):
    room_num = models.IntegerField()
    room_type = models.CharField(max_length=15)
    room_price = models.IntegerField()
    room_status = models.CharField(max_length=15, default='uncheck')

    def __str__(self):
        return 'Room number: ' + str(self.room_num)


class Customs(models.Model):
    custom_name = models.CharField(max_length= 30)
    custom_gender = models.CharField(max_length=5)
    custom_id = models.IntegerField(unique=True, null=True)
    phone_num = models.IntegerField()

    def __str__(self):
        return 'Custom name: ' + self.custom_name


class Bills(models.Model):
    deposit = models.DecimalField(default=0,max_digits=15,decimal_places=2)
    cost = models.DecimalField(default=0,max_digits=15,decimal_places=2)
    reserve_date = models.DateTimeField(null=True,blank=True)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField(null=True,blank=True)
    custom = models.ForeignKey(Customs)
    room = models.ForeignKey(Room)
    #cost_item = models.ForeignKey(Cost_Item, null=True, blank=True)

    def __str__(self):
        return 'Bill id: ' + str(self.id)


class Cost_Item(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    bill = models.ForeignKey(Bills)

    def __str__(self):
        return self.name


class Orders(models.Model):
    custom = models.ForeignKey(Customs)
    room = models.ForeignKey(Room)
    reserve_date = models.DateTimeField()

    def __str__(self):
        return 'Order id:' + str(self.id)


