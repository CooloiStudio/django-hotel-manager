from django.conf.urls import url

from . import views

app_name='RecruitManage'

urlpatterns =[
        url(r'^$', views.position, name='position'),
        url(r'^(?P<position_name>[a-zA-Z]+)/$', views.detail, name='detail'),
        ]