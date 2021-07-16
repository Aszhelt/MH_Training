from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.db.models import Q

from .models import Order, ItemRequest, Storage
from .forms import CreateOrderForm


def orders(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        user_storages = Storage.objects.filter(user_storage=response.user)
        is_multi_storage = user_storages.count() > 1
        not_closed_orders = Order.objects.filter(Q(status_order='D') | Q(status_order='TD')
                                                 | Q(status_order='IP') | Q(status_order='IR'))

        # get not closed orders created by user
        user_orders = not_closed_orders.filter(user_order=response.user)

        # get not closed orders from user`s storage
        orders_from_user_storage = not_closed_orders.filter(storage_from__in=user_storages)

        # get other orders but not closed
        other_orders = not_closed_orders.exclude(storage_from__in=user_storages).\
            exclude(user_order=response.user)

        order_groups = (('My orders', user_orders),
                        ('Orders from my storage', orders_from_user_storage),
                        ('Other orders', other_orders))

        return render(response, 'storage/orders.html',
                      {
                          'is_multi_storage': is_multi_storage,
                          'order_groups': order_groups,
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
        else:
            form = CreateOrderForm()
        return render(response, 'storage/new_order.html',
                      {'form': form})
