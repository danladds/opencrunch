from django import forms
from django.forms.models import ModelChoiceField
from django.forms import DecimalField, CharField, DateField, ModelForm
from django.forms.widgets import DateInput

from ..models import Category

# Add / edit charge (purchase)
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'budget', 'budgetPeriod')
        labels = {
            'name' : 'Label',
            'budget' : 'Budget Amount',
            'budgetPeriod' : 'Budget Period',
        }
        widgets = {

        }
