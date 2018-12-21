from django import forms
from django.forms.models import ModelChoiceField
from django.forms import DecimalField, CharField, DateField, ModelForm
from django.forms.widgets import DateInput

from ..models import Charge, Entity, Invoice, Transaction

# Add / edit charge (purchase)
class ChargeForm(ModelForm):
    class Meta:
        model = Charge
        fields = ('dateMade', 'source', 'description', 'category', 'quantity')
        labels = {
            'dateMade' : 'Date',
            'source' : 'Where From',
            'description' : 'What For',
            'category' : 'Category',
            'quantiy' : 'Amount'
        }
        widgets = {
            'dateMade': DateInput(),
        }

# Add / edit transaction (payment)
class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('dateMade', 'source', 'sink', 'description', 'quantity')
        labels = {
            'dateMade' : 'Date',
            'source' : 'Paid From',
            'sink' : 'Paid To',
            'description' : 'Description',
            'quantity': 'Amount'
        }
        widgets = {
            'dateMade': DateInput(),
        }
    
class UploadFileForm(forms.Form):
    importFile = forms.FileField()



