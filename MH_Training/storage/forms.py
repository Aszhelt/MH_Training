from django import forms
from .models import Item


class CreateNewItem(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'stock', 'image']


class EditItem(forms.Form):
    stock = forms.IntegerField()
