# coding: utf-8

from django.db import models

# Create your models here.


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recruitment(models.Model):
    name = models.CharField(max_length=128, default='name')
    position = models.ForeignKey(Position)
    baseinfo = models.TextField()
    required = models.TextField()

    def __str__(self):
        return str(self.position) + ' ' + str(self.name)

