from django import forms
from django.forms.models import ModelChoiceField 
from django.forms import DecimalField, CharField, DateField, ModelForm
from ..models import Charge, Entity, Invoice, Transaction
from django.forms.widgets import DateInput

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
    
    #description = CharField(label='Description', max_length=1000)
    #quantity = forms.DecimalField(max_digits=12, decimal_places=2, label='Amount')
    #source = ModelChoiceField(queryset=Entity.objects.all(), label='From Whom')
    #date = DateField(label='Date')
    #invoice = ModelChoiceField(queryset=Invoice.objects.all(), label='Invoice')
    
class UploadFileForm(forms.Form):
    importFile = forms.FileField()



