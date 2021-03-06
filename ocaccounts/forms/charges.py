from django import forms
from django.forms.models import ModelChoiceField
from django.forms import DecimalField, CharField, DateField, ModelForm
from django.forms.widgets import DateInput

from ..models import Charge, Entity, Invoice, Transaction

# Add / edit charge (purchase)
class ChargeForm(ModelForm):
    source = forms.ModelChoiceField(queryset=Entity.objects.all().order_by('-fav', 'name'), label='De Donde')

    class Meta:
        model = Charge
        fields = ('dateMade', 'source', 'description', 'category', 'quantity')
        labels = {
            'dateMade' : 'Fecha',
            'description' : 'Para Que',
            'category' : 'Categoría',
            'quantity' : 'Cantidad'
        }
        widgets = {
            'dateMade': DateInput(),
        }

# Add / edit transaction (payment)
class TransactionForm(ModelForm):
    source = forms.ModelChoiceField(queryset=Entity.objects.all().order_by('-fav', 'name'), label='De Donde')
    sink = forms.ModelChoiceField(queryset=Entity.objects.all().order_by('-fav', 'name'), label='A Donde')

    class Meta:
        model = Transaction
        fields = ('dateMade', 'source', 'sink', 'description', 'quantity')
        labels = {
            'dateMade' : 'Fecha',
            'description' : 'Para Que',
            'quantity': 'Cantidad'
        }
        widgets = {
            'dateMade': DateInput(),
        }
    
class UploadFileForm(forms.Form):
    importFile = forms.FileField()



