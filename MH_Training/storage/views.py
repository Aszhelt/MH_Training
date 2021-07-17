import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.db.models import Q
from datetime import date, timedelta

from .models import Order, ItemRequest, Storage, ItemContainer, ItemGroup, Item
from .forms import CreateOrderForm

item_groups = ItemGroup.objects.order_by('sort_priority_item_group')
all_storages = Storage.objects.order_by('-is_public')


def orders(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        user_storages = Storage.objects.filter(user_storage=response.user)
        not_closed_orders = Order.objects.filter(Q(status_order='D') | Q(status_order='TD')
                                                 | Q(status_order='IP') | Q(status_order='IR')).order_by('date_order')

        # get not closed orders to user`s storage
        orders_to_user_storage = not_closed_orders.filter(storage_to__in=user_storages)

        # get not closed orders from user`s storage
        orders_from_user_storage = not_closed_orders.filter(storage_from__in=user_storages)

        # get not closed other orders
        other_orders = not_closed_orders.exclude(storage_from__in=user_storages).exclude(storage_to__in=user_storages)

        today = date.today()
        day_diff_red = today + timedelta(days=1)
        day_diff_yellow = today + timedelta(days=3)

        order_groups = (('Orders to my storage', orders_to_user_storage),
                        ('Orders from my storage', orders_from_user_storage),
                        ('Other orders', other_orders))

        return render(response, 'storage/orders.html',
                      {
                          'order_groups': order_groups,
                          'day_diff_red': day_diff_red,
                          'day_diff_yellow': day_diff_yellow,
                      })


def new_order(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        user_storages = Storage.objects.filter(user_storage=response.user)
        if response.method == 'POST':
            form = CreateOrderForm(response.POST)
            if form.is_valid():
                date_order = form.cleaned_data['date_order']
                storage_from = form.cleaned_data['storage_from']
                storage_to = form.cleaned_data['storage_to']
                user_order = response.user
                order = Order(date_order=date_order, storage_from=storage_from,
                              storage_to=storage_to, user_order=user_order)
                order.save()
                return HttpResponseRedirect('/orders')
        else:
            form = CreateOrderForm()
        return render(response, 'storage/new_order.html',
                      {'form': form})


def storages(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        public_storages = all_storages.filter(is_public=True)
        private_storages = all_storages.filter(is_public=False)
        storage_groups = (
            ('public storages', public_storages),
            ('private storages', private_storages),
        )

        return render(response, 'storage/storages.html',
                      {
                          'storage_groups': storage_groups,
                      })


def storage_view(response, name_storage):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        storage = get_object_or_404(Storage, name_storage=name_storage)
        containers = ItemContainer.objects.filter(storage_container=storage)

        return render(response, 'storage/storage_view.html',
                      {
                          'item_groups': item_groups,
                          'storage': storage,
                          'containers': containers,
                      })
