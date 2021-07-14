from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.db.models import Q

from .models import Order, ItemRequest, Storage


def orders(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        user_orders = Order.objects.filter(user_order=response.user). \
            filter(Q(status_order='D') | Q(status_order='TD')
                   | Q(status_order='IP') | Q(status_order='IR'))  # get not closed orders created by user

        return render(response, 'storage/orders.html',
                      {'user_orders': user_orders})
