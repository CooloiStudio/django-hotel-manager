from django.db import models

# Create your models here.

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recruitment(models.Model):
    position = models.ForeignKey(Position, to_field='name')
    baseinfo = models.TextField()
    required = models.TextField()

    def __str__(self):
        return 'Position detail: ' + str(self.position)

