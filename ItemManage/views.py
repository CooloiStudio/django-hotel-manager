from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from .models import RoomItem,Item
from RoomManage.models import Room

import decimal
# Create your views here.

@login_required()
def index(request):
    room_list = Room.objects.all()
    return render(request,'ItemManage/index.html',{'room_list': room_list})


@login_required()
def add_room_item(request, room_num):
    try:
        item_list = Item.objects.all()
        room = Room.objects.get(room_num=room_num)
    except:
        return HttpResponseRedirect(reverse('ItemManage:index'))

    if request.method == 'POST':
       for item in item_list:
           try:
               amount = int(request.POST['amount_' + str(item.id)])
               price = decimal.Decimal(request.POST['price_' + str(item.id)])
           except:
               return HttpResponseRedirect(reverse('ItemManage:add_room_item', args=(room_num,)))

           if price > 0 and amount > 0:
              room_item_tuple = RoomItem.objects.get_or_create(item_name=item,
                                                               room=room)
              if room_item_tuple[1]:
                  room_item_tuple[0].amount = amount
              else:
                  room_item_tuple[0].amount += amount
              room_item_tuple[0].price = price
              room_item_tuple[0].save()

           elif price == 0 and amount > 0:
              room_item_tuple = RoomItem.objects.get_or_create(item_name=item,
                                                               room=room)
              if room_item_tuple[1]:
                  room_item_tuple[0].amount = amount
              else:
                  room_item_tuple[0].amount += amount
              room_item_tuple[0].save()

       if 'submit' in request.POST:
           return HttpResponseRedirect(reverse('ItemManage:add_room_item', args=(room_num,)))
       elif 'submit_return' in request.POST:
           return HttpResponseRedirect(reverse('ItemManage:index'))

    return render(request,'ItemManage/add_room_item.html',{'item_list': item_list, 'room_num': room_num})


@login_required()
def detail(request, room_num):
    room = Room.objects.get(room_num=room_num)
    item_list = RoomItem.objects.filter(room=room)
    return render(request, 'ItemManage/detail.html', {'item_list':item_list, 'room_num':room_num})

