from django.shortcuts import render
from .models import Item

def storage_main(response):
    items = Item.objects.all()
    return render(response, 'storage/index.html',
                   {'items': items})