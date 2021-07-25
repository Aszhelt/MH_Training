from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.db.models import Q
from datetime import date, timedelta

from .models import Order, ItemRequest, Storage, ItemContainer, ItemGroup
from .forms import CreateOrderForm, CreateRequestForm, EditItemRequest


'''static data'''


item_groups = ItemGroup.objects.order_by('sort_priority_item_group')
today = date.today()


'''main views'''


def storages(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        available_storages = get_available_storages(response)

        return render(response, 'storage/storages.html',
                      {
                          'available_storages': available_storages,
                      })


def orders(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        available_orders = get_available_orders(response)

        day_diff_red = today + timedelta(days=1)
        day_diff_yellow = today + timedelta(days=3)

        return render(response, 'storage/orders.html',
                      {
                          'available_orders': available_orders,
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
                group_order = form.cleaned_data['group_order']
                user_order = response.user
                order = Order(date_order=date_order, storage_from=storage_from,
                              storage_to=storage_to, user_order=user_order, group_order=group_order)
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
        order_functions = get_order_functions(response, order)

        if response.method == 'POST':
            if response.POST.get('save'):
                order_form = CreateOrderForm(response.POST)
                request_form = CreateRequestForm()
                if order_form.is_valid():
                    order.date_order = order_form.cleaned_data['date_order']
                    order.storage_from = order_form.cleaned_data['storage_from']
                    order.storage_to = order_form.cleaned_data['storage_to']
                    order.group_order = order_form.cleaned_data['group_order']
                    order.save()
                    return HttpResponseNotModified()
            else:
                request_form = CreateRequestForm(response.POST)

            data = {
                'date_order': order.date_order,
                'storage_from': order.storage_from,
                'storage_to': order.storage_to,
                'group_order': order.group_order,
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
                              'order_functions': order_functions,
                              'item_groups': item_groups,
                              'order_form': order_form,
                              'request_form': request_form,
                          })
        else:
            data = {
                'date_order': order.date_order,
                'storage_from': order.storage_from,
                'storage_to': order.storage_to,
                'group_order': order.group_order,
            }
            order_form = CreateOrderForm(data=data)

            request_form = CreateRequestForm()
            edit_request_form = CreateRequestForm()

        return render(response, 'storage/view_order.html',
                      {
                          'order': order,
                          'order_functions': order_functions,
                          'item_groups': item_groups,
                          'order_form': order_form,
                          'request_form': request_form,
                          'edit_request_form': edit_request_form
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
            if response.POST.get('Delete'):
                order = item_request.order_request
                item_request.delete()
                return HttpResponseRedirect(f'/orders/{order.id}/')
            form = EditItemRequest(response.POST)
            if form.is_valid():
                item_request.amount_in_request = form.cleaned_data['amount_in_request']
                item_request.save()
                return HttpResponseNotModified()


'''change order status'''


def change_order_status(response, id, status_order):
    status = status_order
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        order = get_object_or_404(Order, pk=id)
        current_status = order.status_order
        if response.method == 'POST':

            if current_status in ('DR', 'TD', 'CR', 'CS', 'CC') and status in ('DR', 'TD', 'CR', 'CS', 'CC'):  # nothing
                order.status_order = status
                order.save()

            elif current_status in ('DR', 'TD', 'CR', 'CS', 'CC') and status in (
            'IP', 'IR', 'L'):  # from storage_from to temp_storage
                checked_storage_from = check_storage_from(order)
                if checked_storage_from['is_enough']:
                    storage_from_to_order(order)
                    order.status_order = status
                    order.save()
                else:
                    order_reduction(order, checked_storage_from)
                    order.status_order = 'DR'
                    order.save()

            elif current_status in ('IP', 'IR', 'L') and (
                    status in ('DR', 'TD', 'CR', 'CS', 'CC')):  # from preparation to storage_from
                order_to_storage_from(order)
                order.status_order = status
                order.save()

            elif current_status in ('IP', 'IR', 'L') and status in ('IP', 'IR', 'L'):  # nothing
                order.status_order = status
                order.save()

            elif current_status in ('IP', 'IR', 'L') and status == 'DN':  # from temp_storage to storage_to
                order_to_storage_to(order)
                order.status_order = status
                order.save()

            elif current_status in ('DR', 'TD', 'CR', 'CS', 'CC') and status == 'DN':  # from storage_from to storage_to
                checked_storage_from = check_storage_from(order)
                if checked_storage_from['is_enough']:
                    storage_from_to_storage_to(order)
                    order.status_order = status
                    order.save()
                else:
                    order_reduction(order, checked_storage_from)
                    order.status_order = 'DR'
                    order.save()

        return HttpResponseRedirect(f'../../orders/{order.id}')


def check_storage_from(order):
    on_storage_from = {'is_enough': True, 'problem_containers': []}
    for order_request in order.order_request.all():

        # check container on storage_from
        if order.storage_from.storage_container.filter(
                item_in_container=order_request.item_in_request).count() == 0:
            # create new container on storage_from
            order.storage_from.storage_container.create(
                item_in_container=order_request.item_in_request,
                amount_in_container=0,
                storage_container=order.storage_to)

        # get container on storage_from
        container_from = order.storage_from.storage_container.get(
            item_in_container=order_request.item_in_request)

        # if enough items on storage_from
        if container_from.amount_in_container < order_request.amount_in_request:
            on_storage_from['is_enough'] = False
            on_storage_from['problem_containers'].append(container_from)

    return on_storage_from


def check_storage_to(order):
    for order_request in order.order_request.all():

        # check container on storage_to
        if order.storage_to.storage_container.filter(
                item_in_container=order_request.item_in_request).count() == 0:
            # create new container on storage_to
            order.storage_to.storage_container.create(
                item_in_container=order_request.item_in_request,
                amount_in_container=0,
                storage_container=order.storage_to)


def get_temp_storage(order):
    if Storage.objects.all().filter(name_storage=f'temporary storage for {order} {order.id}').count() == 0:

        temp_storage = Storage(name_storage=f'temporary storage for {order} {order.id}',
                               user_storage=order.user_order, is_temporary=True)
        temp_storage.save()

        for order_request in order.order_request.all():
            # create new container on temp_storage
            temp_storage.storage_container.create(
                item_in_container=order_request.item_in_request,
                amount_in_container=0,
                storage_container=temp_storage)
    else:
        temp_storage = Storage.objects.all().get(name_storage=f'temporary storage for {order} {order.id}')
    return temp_storage


def order_reduction(order, on_storage_from):
    for container in on_storage_from['problem_containers']:
        order_request = order.order_request.get(item_in_request=container.item_in_container)
        if container.amount_in_container > 0:
            order_request.amount_in_request = container.amount_in_container
            order_request.save()
        else:
            order_request.delete()


def storage_from_to_order(order):
    temp_storage = get_temp_storage(order)

    for order_request in order.order_request.all():
        # get container in storage_from
        container_from = order.storage_from.storage_container.get(
            item_in_container=order_request.item_in_request)

        # get container in temp_storage
        container_temp = temp_storage.storage_container.get(
            item_in_container=order_request.item_in_request)

        container_from.amount_in_container -= order_request.amount_in_request
        container_from.save()

        container_temp.amount_in_container += order_request.amount_in_request
        container_temp.save()

        order_request.status_item_request = 'IP'
        order_request.save()


def order_to_storage_from(order):
    temp_storage = get_temp_storage(order)

    for order_request in order.order_request.all():
        # get container in storage_from
        container_from = order.storage_from.storage_container.get(
            item_in_container=order_request.item_in_request)

        # get container in temp_storage
        container_temp = temp_storage.storage_container.get(
            item_in_container=order_request.item_in_request)

        container_temp.amount_in_container -= order_request.amount_in_request
        container_temp.save()

        container_from.amount_in_container += order_request.amount_in_request
        container_from.save()

        order_request.status_item_request = 'ND'
        order_request.save()


def order_to_storage_to(order):
    check_storage_to(order)
    temp_storage = get_temp_storage(order)

    for order_request in order.order_request.all():
        # get container in storage_to
        container_to = order.storage_to.storage_container.get(
            item_in_container=order_request.item_in_request)

        # get container in temp_storage
        container_temp = temp_storage.storage_container.get(
            item_in_container=order_request.item_in_request)

        container_temp.amount_in_container -= order_request.amount_in_request
        container_temp.save()

        container_to.amount_in_container += order_request.amount_in_request
        container_to.save()

        order_request.status_item_request = 'D'
        order_request.save()

    temp_storage.delete()


def storage_from_to_storage_to(order):
    check_storage_to(order)
    for order_request in order.order_request.all():
        # get container on storage_from
        container_from = order.storage_from.storage_container.get(
            item_in_container=order_request.item_in_request)

        # get container on storage_to
        container_to = order.storage_to.storage_container.get(
            item_in_container=order_request.item_in_request)

        container_from.amount_in_container -= order_request.amount_in_request
        container_from.save()
        container_to.amount_in_container += order_request.amount_in_request
        container_to.save()

        order_request.status_item_request = 'D'
        order_request.save()


'''support functions for storage app views'''


# get statuses for order that current user can set
def get_order_functions(response, order):
    from_status_to_status = {
        'DR': ('TD', 'CC', 'CR', 'IP'),
        'TD': ('DR', 'CC', 'CR', 'CS', 'DN', 'IP'),
        'IP': ('IR', 'DN', 'CS', 'DR', 'TD'),
        'IR': ('L', 'DN'),
        'L': ('DN',),
    }

    sender = order.storage_from.user_storage
    recipient = order.storage_to.user_storage
    creator = order.user_order
    viewer = response.user

    recipient_functions = Order.STATUS_VARS[0][1]
    sender_functions = Order.STATUS_VARS[1][1]
    creator_functions = Order.STATUS_VARS[2][1]

    viewer_functions = {}

    if viewer == creator:
        for pair_functions in creator_functions:
            viewer_functions.update({pair_functions[0]: pair_functions[1]})
    if viewer == recipient:
        for pair_functions in recipient_functions:
            viewer_functions.update({pair_functions[0]: pair_functions[1]})
    if viewer == sender:
        for pair_functions in sender_functions:
            viewer_functions.update({pair_functions[0]: pair_functions[1]})
    print(viewer_functions)

    allowed_functions = {}
    current_status = order.status_order
    if current_status in from_status_to_status:
        functions_set = from_status_to_status[current_status]
    else:
        return allowed_functions

    for function in functions_set:
        if function in viewer_functions.keys():
            allowed_functions.update({function: viewer_functions[function]})

    return allowed_functions


# get available orders that current user can see
def get_available_orders(response):
    user = response.user
    all_orders = Order.objects.order_by('date_order')
    user_groups = user.groups.all()

    not_done_orders = all_orders.filter(Q(status_order='DR') | Q(status_order='TD')
                                        | Q(status_order='IP') | Q(status_order='IR'))

    done_orders = all_orders.exclude(Q(status_order='DR') | Q(status_order='TD')
                                        | Q(status_order='IP') | Q(status_order='IR'))

    if user.is_superuser:
        return {
            'not done orders': not_done_orders,
            'done orders': done_orders,
        }
    else:
        available_storages = get_available_storages(response)
        user_storages = available_storages['my storages']

        orders_in_user_storages = not_done_orders.filter(storage_to__in=user_storages)
        orders_in_user_storages = orders_in_user_storages.union(
            not_done_orders.filter(storage_from__in=user_storages)
        )

        dict_of_orders_groups = {'orders in my storages': orders_in_user_storages}

        for user_group in user_groups:
            group_orders = get_group_orders(response, user_group)
            dict_of_orders_groups.update({
                f'{user_group.name} orders': group_orders[f'{user_group.name} orders']
            })

        return dict_of_orders_groups


# get all orders related to group
def get_group_orders(response, user_group):
    all_orders = Order.objects.order_by('date_order')
    not_done_orders = all_orders.filter(Q(status_order='DR') | Q(status_order='TD')
                                        | Q(status_order='IP') | Q(status_order='IR'))

    orders_in_group_storages = not_done_orders.filter(group_order=user_group)

    group_orders = {f'{user_group.name} orders': orders_in_group_storages}
    return group_orders


# get available storages that current user can see
def get_available_storages(response):

    user = response.user
    all_storages = Storage.objects.order_by('-is_public')
    user_groups = user.groups.all()

    if user.is_superuser:
        not_temporary_storages = all_storages.exclude(is_temporary=True)
        temporary_storages = all_storages.exclude(is_temporary=False)
        return {
            'not temporary storages': not_temporary_storages,
            'temporary storages': temporary_storages,
        }

    else:
        all_storages = all_storages.exclude(is_temporary=True)
        dict_of_storages_groups = {'my storages': all_storages.filter(user_storage=user)}

        for user_group in user_groups:
            all_storages_in_group = get_group_storages(response, user_group)

            dict_of_storages_groups.update({
                f'{user_group.name} storages': all_storages_in_group[f'{user_group.name} storages']
            })

        return dict_of_storages_groups


# get all storages related to group
def get_group_storages(response, user_group):

    all_storages = Storage.objects.order_by('-is_public').exclude(is_temporary=True)

    group_storages = {f'{user_group.name} storages': all_storages.filter(groups_storage=user_group)}

    return group_storages
