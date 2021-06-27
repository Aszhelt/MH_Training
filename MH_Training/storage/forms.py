from django import forms
from .models import Item


class CreateNewItem(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'stock', 'image', 'tags']


class EditItem(forms.Form):
    stock = forms.IntegerField()
