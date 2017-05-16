from django.conf.urls import url

from . import views

app_name = 'ItemManage'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_num>[0-9]+)/$', views.add_room_item, name='add_room_item'),
    url(r'^(?P<room_num>[0-9]+)/detail/$', views.detail, name='detail'),
]