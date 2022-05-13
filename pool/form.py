import datetime

from django import forms

from pool.models import *


class GenerateVoucherForm(forms.Form):
    offers = forms.ModelChoiceField(queryset=SpecialOffer.objects.all())
    expiry_date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
