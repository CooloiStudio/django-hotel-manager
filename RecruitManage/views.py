# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from .models import Position, Recruitment
# Create your views here.

title = '招聘管理'

def position(request):
    recruitment_list = Recruitment.objects.all()
    context = {
        'title': title,
        'recruitment_list': recruitment_list,
    }
    return render(request, 'RecruitManage/recruitment.html', {'recruitment_list': recruitment_list})


def detail(request, recruitment_id):
    recruitment = get_object_or_404(Recruitment, id=recruitment_id)
    context = {
        'title': title,
        'recruitment': recruitment,
    }
    return render(request, 'RecruitManage/detail.html', {'recruitment': recruitment})