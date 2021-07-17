from django import forms
from .models import Storage, Item


class CreateOrderForm(forms.Form):

    date_order = forms.DateField(widget=forms.SelectDateWidget())
    storage_from = forms.ModelChoiceField(queryset=Storage.objects.all())
    storage_to = forms.ModelChoiceField(queryset=Storage.objects.all())

    def clean(self):
        cleaned_data = super(CreateOrderForm, self).clean()
        if cleaned_data['storage_from'] == cleaned_data['storage_to']:
            raise forms.ValidationError("Storages match")
        return cleaned_data


class CreateRequestForm(forms.Form):
    item_in_request = forms.ModelChoiceField(queryset=Item.objects.all())
    amount_in_request = forms.IntegerField(min_value=1, max_value=9999)


class EditItemRequest(forms.Form):
    amount_in_request = forms.IntegerField(min_value=1, max_value=9999)
