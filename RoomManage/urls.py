# coding: utf-8

from django.conf.urls import url

from . import views

app_name = 'RoomManage'

urlpatterns = [
    url(r'^$', views.index, name='index'),  # 房间管理首页
    url(r'^check/$', views.check, name='check'),  # 未被预定或入住的房间列表
    url(r'^check/(?P<room_num>[0-9]+)/reserve/$', views.custom_reserve, name='custom_reserve'),  # 预定房间
    url(r'^check/(?P<room_num>[0-9]+)/check_in/$', views.custom_check_in, name='custom_check_in'),  # 入住房间
    url(r'^checkreserved/$', views.check_reserved, name='check_reserved'),  # 已被预定房间列表
    url(r'^unreserved/(?P<room_num>[0-9]+)/$', views.custom_unreserved, name='unreserved'),  # 退订房间
    url(r'^checkout/$', views.checkout, name='checkout'),  # 可退房的房间列表
    url(r'^checkout/(?P<room_num>[0-9]+)/$', views.custom_checkout, name='custom_checkout'),  # 退房
    url(r'^roomstatus/$', views.room_status, name='room_status'),  # 房间状态列表
    url(r'^roomstatus/(?P<room_num>[0-9]+)/$', views.detail, name='detail'),  # 房间状态详情
]
