# coding: utf-8

from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Task, Attendance, Emergency
from RoomManage.models import Room
from RoomManage.views import Room_Status

# Create your views here.


@login_required()
def index(request):
    clock_status = True
    if request.method == 'POST':
        if 'clockin' in request.POST:
            attendance = Attendance.objects.create(clock_in=timezone.now(),
                                                   clock_out=None,
                                                   user=request.user)
            attendance.save()
            return render(request,'TaskManage/index.html',{'clock_status':False})
        elif 'clockout' in request.POST:
            attendance = Attendance.objects.filter(user=request.user).get(clock_out=None)
            attendance.clock_out = timezone.now()
            attendance.save()
            return render(request, 'TaskManage/index.html', {'clock_status': True})

    try:
        if Attendance.objects.filter(user=request.user).get(clock_out=None):
            clock_status =False
    except:
        pass
    
    return render(request,'TaskManage/index.html',{'clock_status': clock_status})


@login_required()
def tasklist(request):
    task_list = Task.objects.filter(user=request.user.id).exclude(task_status=task_status.done)
    if task_list is None:
        return render(request,'TaskManage/index.html')

    return render(request,'TaskManage/tasklist.html',{'task_list': task_list})


@login_required()
def detail(request, task_num):
    task = Task.objects.get(id=task_num)
    if request.user.id != task.user.id:
        return HttpResponseRedirect(reverse('TaskManage:tasklist'))

    if request.method == 'POST' :
        if request.POST['done']:
            task.task_status = task_status.done
            task.save()
        return HttpResponseRedirect(reverse('TaskManage:detail',args=(task_num,)))

    return render(request,'TaskManage/detail.html',{'task': task})


@login_required()
@permission_required('Emergency.create_emergency')
def emergency(request):
    room_list = Room.objects.filter(room_status=room_status.check_ing)
    user_list = User.objects.all().exclude(is_superuser=True)

    if request.method == 'POST':
        user_id = request.POST['user_id']
        room_id = request.POST['room_id']

        date = timezone.now()
        user = user_list.get(id=user_id)
        room = room_list.get(id=room_id)
        emer = Emergency.objects.create(date_time=date,
                                        user=user,
                                        room=room)
        emer.save()
        create_task(user, room, date)

        if 'submit' in request.POST:
            return HttpResponseRedirect(reverse('TaskManage:emergence'))
        elif 'submit_return' in request.POST:
            return HttpResponseRedirect(reverse('TaskManage:index'))

    return render(request, 'TaskManage/emergency.html', {'room_list':room_list, 'user_list':user_list})


def create_task(user, room, date):

    task = Task.objects.create(user=user,
                               room=room,
                               date=date,
                               context='Emergency',
                               task_status=task_status.undo)
    task.save()

class Task_Status(object):
    def __init__(self):
        self.done = 'done'
        self.undo = 'undo'

task_status = Task_Status()

room_status = Room_Status()
