from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .models import Item
from django.http import HttpResponseRedirect
from .forms import CreateNewItem, EditItem


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
        if response.method == 'POST':
            form = EditItem(response.POST)
            if form.is_valid():
                item.stock = form.cleaned_data['stock']
                item.save()
                return HttpResponseRedirect('/storage')
        else:
            form = EditItem()
        return render(response, 'storage/view_item.html',
                       {'item': item, 'form': form})
    else:
        return HttpResponseRedirect('/login')


def create_item(response):
    if response.user.is_authenticated:
        if response.method == "POST":
            form = CreateNewItem(response.POST, response.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/storage')
        else:
            form = CreateNewItem()
        return render(response, "storage/create_item.html", {"form": form})
    else:
        return HttpResponseRedirect('/login')