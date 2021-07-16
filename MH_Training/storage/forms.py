from django import forms
from .models import Storage


class CreateOrderForm(forms.Form):
    date_order = forms.DateField(widget=forms.SelectDateWidget())
    storage_from = forms.ModelChoiceField(queryset=Storage.objects.all())
    storage_to = forms.ModelChoiceField(queryset=Storage.objects.all())
