from django import forms
from django.forms.models import ModelChoiceField
from django.forms import DecimalField, CharField, DateField, ModelForm
from django.forms.widgets import DateInput

from ..models import Charge, Entity, Invoice, Transaction

# Add / edit charge (purchase)
class ChargeForm(ModelForm):
    source = forms.ModelChoiceField(queryset=Entity.objects.all().order_by('-fav', 'name'), label='Where From')

    class Meta:
        model = Charge
        fields = ('dateMade', 'source', 'description', 'category', 'quantity')
        labels = {
            'dateMade' : 'Date',
            'description' : 'What For',
            'category' : 'Category',
            'quantity' : 'Amount'
        }
        widgets = {
            'dateMade': DateInput(),
        }

# Add / edit transaction (payment)
class TransactionForm(ModelForm):
    source = forms.ModelChoiceField(queryset=Entity.objects.all().order_by('-fav', 'name'), label='Where From')
    sink = forms.ModelChoiceField(queryset=Entity.objects.all().order_by('-fav', 'name'), label='Where To')

    class Meta:
        model = Transaction
        fields = ('dateMade', 'source', 'sink', 'description', 'quantity')
        labels = {
            'dateMade' : 'Date',
            'description' : 'Description',
            'quantity': 'Amount'
        }
        widgets = {
            'dateMade': DateInput(),
        }
    
class UploadFileForm(forms.Form):
    importFile = forms.FileField()



