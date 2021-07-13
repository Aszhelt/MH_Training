from django import forms
from .models import Item, Event, Storage, ItemRequest


class CreateNewRequestItem(forms.ModelForm):

    class Meta:
        model = ItemRequest
        fields = ['item_request', 'amount_item_request', 'event_item_request',
                  'storage_out', 'storage_in', 'status']


class EditRequestItem(forms.Form):
    item_request = forms.ModelChoiceField(Item.objects.all())
    amount_item_request = forms.IntegerField(min_value=0, max_value=9999)
    storage_out = forms.ModelChoiceField(Storage.objects.all())
    storage_in = forms.ModelChoiceField(Storage.objects.all())


class CreateNewEvent(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name_event', 'date_event']
