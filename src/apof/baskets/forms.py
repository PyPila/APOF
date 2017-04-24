from django import forms


class ConfirmBasketForm(forms.Form):
    value = forms.BooleanField()
