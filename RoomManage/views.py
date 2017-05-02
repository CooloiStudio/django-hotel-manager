from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Room,Customs,Bills,Orders,Cost_Item
from ItemManage.models import RoomItem,Item

import decimal

# Create your views here.


def index(request):
    return render(request,'RoomManage/index.html')


@login_required()
def check(request):
    room_list = Room.objects.filter(room_status=status.uncheck)
    return  render(request,'RoomManage/check.html',{'room_list':room_list})


@login_required()
def check_reserved(request):
    room_list = Room.objects.filter(room_status=status.reserved)
    return render(request, 'RoomManage/check_reserve.html', {'room_list': room_list})


@login_required()
def custom_checkin(request, room_num):
    try:
        room = Room.objects.get(room_num=room_num)
        if room.room_status == status.checking:
            raise KeyError
    except:
        return HttpResponseRedirect(reverse('RoomManage:check'))

    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        id = request.POST['id']
        phone_num = request.POST['phone_num']
        try:
            cus = Customs.objects.get_or_create(custom_name=name,
                                                custom_gender=gender,
                                                phone_num=phone_num)
            if cus[1]:
                cus[0].custom_id = id
                cus[0].save()

            create_checkin_bill(cus[0], room)
            return HttpResponseRedirect(reverse('RoomManage:detail', args=(room_num,)))
        except:
            return render(request, 'RoomManage/custom_checkin.html', {'message': 'don`t submit blank', 'room_num':room_num})

    return render(request, 'RoomManage/custom_checkin.html', {'room_num':room_num})


@login_required()
def custom_reserve(request, room_num):
    try:
        room = Room.objects.get(room_num=room_num)
        if room.room_status != status.uncheck:
            raise KeyError
    except:
        return HttpResponseRedirect(reverse('RoomManage:check'))

    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        phone_num = request.POST['phone_num']

        try:
            cus = Customs.objects.get_or_create(custom_name=name,
                                                custom_gender=gender,
                                                phone_num=phone_num)
            if cus[1] : cus[0].save()
            create_order(cus[0],room)
            return HttpResponseRedirect(reverse('RoomManage:detail', args=(room_num,)))
        except:
            return render(request, 'RoomManage/custom_reserve.html', {'message': 'don`t submit blank', 'room_num': room_num})

    return render(request, 'RoomManage/custom_reserve.html', {'room_num': room_num})


@login_required()
def checkout(request):
    room_list = Room.objects.filter(room_status=status.checking)
    return render(request,'RoomManage/checkout.html',{'room_list':room_list})


@login_required()
def custom_checkout(request,room_num):
    try:
        room = Room.objects.get(room_num=room_num)
        items_list = RoomItem.objects.filter(room=room)
        if room.room_status != status.checking:
            raise KeyError
    except:
        return HttpResponseRedirect(reverse('RoomManage:checkout'))

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
        return render(request, 'RoomManage/custom_checkout.html', {'bill':bill,'cost_item_list':cost_item_list})

    return render(request, 'RoomManage/custom_checkout.html', {'items_list':items_list, 'room_num':room_num})


@login_required()
def room_status(request):
    room_list = Room.objects.all().order_by('room_num')
    return render(request,'RoomManage/room_status.html',{'room_list':room_list})


@login_required()
def detail(request,room_num):
    try:
        room = Room.objects.get(room_num=room_num)
    except:
        return HttpResponseRedirect(reverse('RoomManage:room_status'))

    context = room_context(room)
    return render(request, 'RoomManage/detail.html',context)


class Room_Status(object):
    def __init__(self):
        self.uncheck = 'uncheck'
        self.checking = 'checking'
        self.reserved = 'reserved'

status = Room_Status()


def room_context(room):
    if room.room_status == status.uncheck:
        message = 'there no order and on one checkin'
        return {'message': message, 'room': room}
    elif room.room_status == status.reserved:
        message = 'this room has been reserved'
        order = Orders.objects.get(room=room.id) # try?
        custom = Customs.objects.get(id=order.custom.id)
        return {'message': message,'order': order,'custom': custom,'room': room}
    elif room.room_status == status.checking:
        message = 'this room has checking'
        bill = Bills.objects.get(room=room.id)
        custom = Customs.objects.get(id=bill.custom.id)
        return {'message': message,'bill': bill,'custom': custom,'room': room}
    else:
        return {'message': 'Room status is error'}


def create_order(custom, room):
    try:
        order = Orders.objects.create(reserve_date = timezone.now(),
                                       room=room,
                                       custom=custom)
        room.room_status=status.reserved
        order.save()
        room.save()
        return order.id
    except:
        pass


def create_checkin_bill(custom, room):
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
    room.room_status = status.checking
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
