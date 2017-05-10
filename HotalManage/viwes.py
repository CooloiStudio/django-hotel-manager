from django.shortcuts import render

from RecruitManage.models import Recruitment
from TaskManage.models import Task
from TaskManage.views import task_status

def home(request):
   recruitment_list = Recruitment.objects.all()[:3]
   task_list = Task.objects.filter(task_status=task_status.undo)

   return render(request, 'home.html', {'recruitment_list': recruitment_list, 'task_list': task_list})