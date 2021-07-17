from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.db.models import Q
from datetime import date, timedelta

from .models import Order, ItemRequest, Storage, ItemContainer, ItemGroup, Item
from .forms import CreateOrderForm, CreateRequestForm, EditItemRequest

item_groups = ItemGroup.objects.order_by('sort_priority_item_group')
all_storages = Storage.objects.order_by('-is_public')
today = date.today()


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
                return HttpResponseRedirect(f'/orders/{order.id}')
        else:
            form = CreateOrderForm(initial={'date_order': today})
        return render(response, 'storage/new_order.html',
                      {'form': form})


def view_order(response, id):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        order = get_object_or_404(Order, id=id)

        if response.method == 'POST':
            if response.POST.get('save'):
                order_form = CreateOrderForm(response.POST)
                request_form = CreateRequestForm()
                if order_form.is_valid():
                    order.date_order = order_form.cleaned_data['date_order']
                    order.storage_from = order_form.cleaned_data['storage_from']
                    order.storage_to = order_form.cleaned_data['storage_to']
                    order.save()
                    return HttpResponseNotModified()
            else:
                request_form = CreateRequestForm(response.POST)

            data = {
                'date_order': order.date_order,
                'storage_from': order.storage_from,
                'storage_to': order.storage_to
            }
            order_form = CreateOrderForm(data=data)

            if response.POST.get('NewItem'):
                if request_form.is_valid():
                    item_in_request = request_form.cleaned_data['item_in_request']
                    amount_in_request = request_form.cleaned_data['amount_in_request']
                    if order.order_request.filter(item_in_request=item_in_request):
                        print("invalid")
                    else:
                        order.order_request.create(item_in_request=item_in_request,
                                                   amount_in_request=amount_in_request)

            return render(response, 'storage/view_order.html',
                          {
                              'order': order,
                              'item_groups': item_groups,
                              'order_form': order_form,
                              'request_form': request_form,
                          })
        else:
            data = {
                'date_order': order.date_order,
                'storage_from': order.storage_from,
                'storage_to': order.storage_to
            }
            order_form = CreateOrderForm(data=data)

            request_form = CreateRequestForm()
            edit_request_form = CreateRequestForm()

        return render(response, 'storage/view_order.html',
                      {
                          'order': order,
                          'item_groups': item_groups,
                          'order_form': order_form,
                          'request_form': request_form,
                          'edit_request_form': edit_request_form
                      })


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


def edit_item_request(response, id):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        item_request = get_object_or_404(ItemRequest, pk=id)
        if response.method == 'POST':
            form = EditItemRequest(response.POST)
            if response.POST.get('Delete'):
                order = item_request.order_request
                item_request.delete()
                return HttpResponseRedirect(f'/orders/{order.id}/')
            elif form.is_valid():
                item_request.amount_in_request = form.cleaned_data['amount_in_request']
                item_request.save()
                return HttpResponseNotModified()
