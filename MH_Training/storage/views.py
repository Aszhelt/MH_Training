from django.shortcuts import render, get_object_or_404

from .models import Item, Tag, GroupTag
from django.http import HttpResponseRedirect
from .forms import CreateNewItem, EditItem


group_tags = (GroupTag.objects.get(name='Critical_bleeding'), GroupTag.objects.get(name='Airways'),
                      GroupTag.objects.get(name='Breathing'), GroupTag.objects.get(name='Circulation'))


def storage_main(response):
    if response.user.is_authenticated:
        group_tags
        return render(response, 'storage/index.html',
                       {'group_tags': group_tags})
    else:
        return HttpResponseRedirect('/login')


def view_group(response, name):
    if response.user.is_authenticated:
        tags = Tag.objects.filter(group__name=name)
        items = Item.objects.order_by('tags')
        name = name.replace('_', ' ')
        return render(response, 'storage/view_group.html',
                       {'items': items, 'tags': tags,
                        'name': name, 'group_tags': group_tags})
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