from django.shortcuts import render, get_object_or_404
from .models import Item
from django.http import HttpResponseRedirect


def storage_main(response):
    if response.user.is_authenticated:
        items = Item.objects.all()
        return render(response, 'storage/index.html',
                       {'items': items})
    else:
        return HttpResponseRedirect('/login')


def view_item(response, id):
    if response.user.is_authenticated:
        item = get_object_or_404(Item, pk=id)
        return render(response, 'storage/view_item.html',
                       {'item': item})
    else:
        return HttpResponseRedirect('/login')
