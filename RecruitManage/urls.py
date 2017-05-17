# coding: utf-8

from django.conf.urls import url

from . import views

app_name = 'RecruitManage'

urlpatterns = [
    url(r'^$', views.position, name='position'),
    url(r'^(?P<recruitment_id>[0-9]+)/$', views.detail, name='detail'),
]
