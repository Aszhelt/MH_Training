from django import forms


class EditItem(forms.Form):
    item_stock = forms.IntegerField()
