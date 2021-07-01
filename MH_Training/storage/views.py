from django.shortcuts import render, get_object_or_404

from .models import Item, ItemType, ItemGroup
from django.http import HttpResponseRedirect, HttpResponseNotModified
from .forms import EditItem

item_groups = ItemGroup.objects.order_by('item_group_sort_priority')
item_types = ItemType.objects.order_by('item_type_sort_priority')


def storage_main(response):
    if response.user.is_authenticated:
        return render(response, 'storage/index.html',
                       {'item_groups': item_groups})
    else:
        return HttpResponseRedirect('/login')


def view_group(response, item_group_name):
    if response.user.is_authenticated:
        item_group = item_groups.get(item_group_name=item_group_name)
        items = Item.objects.filter(item_group=item_group)
        ret_item_types = []
        for item in items:
            ret_item_types.append(item.item_type)
        ret_item_types = set(ret_item_types)
        return render(response, 'storage/view_group.html',
                       {'items': items, 'item_types': ret_item_types,
                        'item_group_name': item_group_name, 'item_groups': item_groups})
    else:
        return HttpResponseRedirect('/login')


def view_item(response, id):
    if response.user.is_authenticated:
        item = get_object_or_404(Item, pk=id)
        if response.method == 'POST':
            form = EditItem(response.POST)
            if form.is_valid():
                item.item_stock = form.cleaned_data['item_stock']
                item.save()
                return HttpResponseNotModified()
        else:
            form = EditItem()
        return render(response, 'storage/view_item.html',
                       {'item': item, 'form': form})
    else:
        return HttpResponseRedirect('/login')
