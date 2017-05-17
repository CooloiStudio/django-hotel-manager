# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from RoomManage.models import Room, Customs
# Create your models here.

class Task(models.Model):
    context = models.TextField()
    date = models.DateTimeField()
    task_status = models.CharField(max_length=20,default='undo')
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room)

    def __str__(self):
        return str(self.user.first_name) + ' datetime:' + str(self.date)


class Attendance(models.Model):
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True,blank=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.user.first_name + ' date: ' + str(self.clock_in)


class Emergency(models.Model):
    date_time = models.DateTimeField()
    room = models.ForeignKey(Room)
    user = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return 'date time:' + str(self.date_time)

    class Meta:
        permissions = (
            ('create_emergency', 'can create a emergency'),
        )