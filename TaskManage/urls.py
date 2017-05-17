# coding: utf-8

from django.conf.urls import url

from . import views

app_name = 'TaskManage'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^tasklist/$',views.tasklist,name='tasklist'),
    url(r'^tasklist/(?P<task_num>[0-9]+)/$',views.detail,name='detail'),
    url(r'^emergence/$', views.emergency, name='emergence'),
]