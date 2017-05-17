# coding: utf-8

from django.shortcuts import render

from RecruitManage.models import Recruitment
from TaskManage.models import Task
from TaskManage.views import task_status


def home(request):
    template = 'home.html'
    recruitment_list = Recruitment.objects.all()[:4]
    task_list = Task.objects.filter(task_status=task_status.undo)

    context = {
        'title': 'One酒店管理',
        'recruitment_list': recruitment_list,
        'task_list': task_list
    }
    return render(request, template, context)
