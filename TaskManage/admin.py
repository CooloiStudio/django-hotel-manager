# coding: utf-8

from django.contrib import admin

from .models import Task,Attendance,Emergency
# Register your models here.
admin.site.register(Task)
admin.site.register(Attendance)
admin.site.register(Emergency)