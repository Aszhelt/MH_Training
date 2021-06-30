from django import forms


class EditItem(forms.Form):
    stock = forms.IntegerField()
