# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from .models import Position, Recruitment
# Create your views here.


def position(request):
    recruitment_list = Recruitment.objects.all()
    return render(request, 'RecruitManage/recruitment.html', {'recruitment_list': recruitment_list})


def detail(request, recruitment_id):
    recruitment = get_object_or_404(Recruitment, id=recruitment_id)
    return render(request, 'RecruitManage/detail.html', {'recruitment': recruitment})