from django.shortcuts import render, get_object_or_404

from .models import ItemType, ItemGroup, Item, Storage, ItemContainer, Event, ItemRequest
from django.http import HttpResponseRedirect, HttpResponseNotModified
from .forms import CreateNewRequestItem, CreateNewEvent, EditRequestItem


def create_item_request(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        action = "/item_request/create/"
        if response.method == "POST":
            form = CreateNewRequestItem(response.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/item_request/create')
        else:
            form = CreateNewRequestItem()
        return render(response, "storage/create.html", {"form": form, "action": action})


def create_event(response): #google forms.DateField(widget = forms.SelectDateWidget)
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        action = "/event/create/"
        if response.method == "POST":
            form = CreateNewEvent(response.POST)
            if form.is_valid():
                name_event = form.cleaned_data["name_event"]
                date_event = form.cleaned_data["date_event"]
                user_event = response.user
                new_event = Event(name_event=name_event, date_event=date_event,
                                  user_event=user_event)
                new_event.save()
                return HttpResponseRedirect('/event/create')
        else:
            form = CreateNewEvent()
        return render(response, "storage/create.html", {"form": form, "action": action})


def events(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        events = Event.objects.filter(user_event=response.user)
        return render(response, 'storage/events.html',
                      {'events': events})


def view_event(response, id):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        action = f"/event/{id}/"
        event = get_object_or_404(Event, pk=id)
        item_requests = ItemRequest.objects.filter(event_item_request=event)

        forms = []
        for item_request in item_requests:
            form = EditRequestItem()
            form.fields['item_request'].initial = item_request.item_request
            form.fields['amount_item_request'].initial = item_request.amount_item_request
            form.fields['storage_out'].initial = item_request.storage_out
            form.fields['storage_in'].initial = item_request.storage_in
            forms.append((item_request.id, form))
        return render(response, 'storage/view_event.html',
                      {'event': event, 'item_requests': item_requests,
                       'forms': forms, 'action': action})


def view_item_request(response, id):
    if not response.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        item_request = get_object_or_404(ItemRequest, pk=id)
        action = f"/item_request/{id}/"

        if response.method == 'POST':
            form = EditRequestItem(response.POST)
            if form.is_valid():
                item_request.item_request = form.cleaned_data["item_request"]
                item_request.amount_item_request = form.cleaned_data["amount_item_request"]
                item_request.storage_out = form.cleaned_data["storage_out"]
                item_request.storage_in = form.cleaned_data["storage_in"]
                item_request.save()
                return HttpResponseNotModified()
        else:
            form = EditRequestItem()
            form.fields['item_request'].initial = item_request.item_request
            form.fields['amount_item_request'].initial = item_request.amount_item_request
            form.fields['storage_out'].initial = item_request.storage_out
            form.fields['storage_in'].initial = item_request.storage_in
        return render(response, 'storage/edit_request.html',
                      {'item_request': item_request, 'form': form,
                       'action': action})
