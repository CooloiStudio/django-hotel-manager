# coding: utf-8

from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Room, Customs, Bills, Orders, Cost_Item
from ItemManage.models import RoomItem, Item

import decimal

# Create your views here.

title = '客房管理'


def index(request):
    context = {
        'title': title
    }
    return render(request,
                  'RoomManage/index.html',
                  context)


@login_required()
def check(request):
    room_list = Room.objects.filter(room_status=status.uncheck)

    context = {
        'title': title,
        'room_list': room_list
    }

    return render(request, 'RoomManage/check.html', context)


@login_required()
def check_reserved(request):
    room_list = Room.objects.filter(room_status=status.reserved)
    context = {
        'title': title,
        'room_list': room_list
    }
    return render(request, 'RoomManage/check_reserve.html', context)


@login_required()
def custom_check_in(request, room_num):
    try:
        room = Room.objects.get(room_num=room_num)
        if room.room_status == status.check_ing:
            raise KeyError

    except:
        return HttpResponseRedirect(reverse('RoomManage:check'))

    template_name = 'RoomManage/custom_check_in.html'

    context = {
        'title': title,
        'room_num': room_num
    }

    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        identity = request.POST['id']
        phone_num = request.POST['phone_num']
        try:
            cus = Customs.objects.get_or_create(custom_name=name,
                                                custom_gender=gender,
                                                phone_num=phone_num)
            if cus[1]:
                cus[0].custom_id = identity
                cus[0].save()

            create_check_in_bill(cus[0], room)
            return HttpResponseRedirect(reverse('RoomManage:detail', args=(room_num,)))
        except:
            context = dict({'message': 'don`t submit blank'}, **context)

    return render(request, template_name, context)


@login_required()
def custom_reserve(request, room_num):
    try:
        room = Room.objects.get(room_num=room_num)
        if room.room_status != status.uncheck:
            raise KeyError
    except:
        return HttpResponseRedirect(reverse('RoomManage:check'))

    template_name = 'RoomManage/custom_reserve.html'

    context = {
        'title': title,
        'room_num': room_num
    }

    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        phone_num = request.POST['phone_num']

        try:
            cus = Customs.objects.get_or_create(custom_name=name,
                                                custom_gender=gender,
                                                phone_num=phone_num)
            if cus[1]: cus[0].save()
            create_order(cus[0], room)
            return HttpResponseRedirect(reverse('RoomManage:detail', args=(room_num,)))
        except:
            context = dict({'message': 'don`t submit blank'}, **context)

    return render(request, template_name, context)


@login_required()
def checkout(request):
    room_list = Room.objects.filter(room_status=status.check_ing)

    context = {
        'title': title,
        'room_list': room_list
    }
    return render(request, 'RoomManage/checkout.html', context)


@login_required()
def custom_checkout(request, room_num):
    try:
        room = Room.objects.get(room_num=room_num)
        items_list = RoomItem.objects.filter(room=room)
        if room.room_status != status.check_ing:
            raise KeyError
    except:
        return HttpResponseRedirect(reverse('RoomManage:checkout'))

    template_name = 'RoomManage/custom_checkout.html'

    if request.method == 'POST':
        cost_dict = dict()
        for item in items_list:
            try:
                amount = int(request.POST[str(item.id)])
                if amount != 0:
                    cost_dict[str(item.id)] = amount
            except:
                pass
        bill = create_checkout_bill(room=room, cost_dict=cost_dict, items_list=items_list)
        room.room_status = status.uncheck
        room.save()
        cost_item_list = Cost_Item.objects.filter(bill=bill)
        context = {
            'title': title,
            'bill': bill,
            'cost_item_list': cost_item_list
        }
        return render(request, template_name, context)

    context = {
        'title': title,
        'items_list': items_list,
        'room_num': room_num
    }
    return render(request, template_name, context)


@login_required()
def room_status(request):
    room_list = Room.objects.all().order_by('room_num')
    context = {
        'title': title,
        'room_list': room_list
    }
    return render(request, 'RoomManage/room_status.html', context)


@login_required()
def detail(request, room_num):
    try:
        room = Room.objects.get(room_num=room_num)
    except:
        return HttpResponseRedirect(reverse('RoomManage:room_status'))

    context = dict({'title': title}, **room_context(room))
    return render(request, 'RoomManage/detail.html', context)


class Room_Status(object):
    def __init__(self):
        self.uncheck = 'uncheck'
        self.check_ing = 'check_ing'
        self.reserved = 'reserved'


status = Room_Status()


def room_context(room):
    if room.room_status == status.uncheck:
        message = '未入住 未产生账单'
        return {'message': message, 'room': room}
    elif room.room_status == status.reserved:
        message = '该客房被已被预定'
        order = Orders.objects.get(room=room.id)  # try?
        custom = Customs.objects.get(id=order.custom.id)
        return {'message': message, 'order': order, 'custom': custom, 'room': room}
    elif room.room_status == status.check_ing:
        message = '该客房已被入住'
        bill = Bills.objects.get(room=room.id)
        custom = Customs.objects.get(id=bill.custom.id)
        return {'message': message, 'bill': bill, 'custom': custom, 'room': room}
    else:
        return {'message': '信息获取有误，请联系管理员'}


def create_order(custom, room):
    try:
        order = Orders.objects.create(reserve_date=timezone.now(),
                                      room=room,
                                      custom=custom)
        room.room_status = status.reserved
        order.save()
        room.save()
        return order.id
    except:
        pass


def create_check_in_bill(custom, room):
    reserve_date = None

    try:
        order_list = Orders.objects.filter(custom=custom).filter(room=room)
        for order in order_list:
            if order.room.room_status == status.reserved:
                reserve_date = order.reserve_date
    except:
        pass
    bill = Bills.objects.create(deposit=100,
                                cost=room.room_price,
                                reserve_date=reserve_date,
                                check_in_date=timezone.now(),
                                custom=custom,
                                room=room)
    room.room_status = status.check_ing
    room.save()
    bill.save()
    return bill.id


def create_checkout_bill(room, cost_dict, items_list):
    check_out_date = timezone.now()
    try:
        bill = Bills.objects.filter(check_out_date=None).get(room=room)
    except:
        return None

    count = (check_out_date - bill.check_in_date).days
    if count < 1:
        count = 1
    cost = count * room.room_price
    if cost_dict:
        cost += create_cost_item(cost_dict, items_list, bill)

    bill.check_out_date = check_out_date
    bill.cost = cost
    bill.save()
    return bill


def create_cost_item(cost_dict, items_list, bill):
    cost = decimal.Decimal('0.0')
    for key in cost_dict:
        item = items_list.get(id=key)
        cost += item.price * cost_dict[key]
        cost_item = Cost_Item.objects.create(name=item.item_name.name,
                                             amount=cost_dict[key],
                                             price=item.price,
                                             bill=bill)
        cost_item.save()
        total_item = Item.objects.get(name=item.item_name.name)
        if total_item.amount > cost_dict[key]:
            total_item.amount -= cost_dict[key]
            total_item.save()
        else:
            total_item.amount = 0
            total_item.save()

    return cost
