from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse_lazy
from ..models import Entity, Category
from decimal import Decimal, ROUND_UP
from ..forms import UploadFileForm

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        
        totalbalance = Decimal('0.00')
        totalBudget = Decimal('0.00')
        totalSpend = Decimal('0.00')
        remainingBudget = Decimal('0.00')
        
        for entity in Entity.objects.all():
            totalbalance = totalbalance + entity.balance
        
        for category in Category.objects.all():
            if (category.budgetPeriod == 'L'): continue
            if (category.budgetPeriod == 'Y'): continue
            if (category.fixed == True): continue
            totalBudget = category.scaleBudget(('M')) + totalBudget
            totalSpend = category.getSpend('M') + totalSpend
            
        remainingBudget = totalBudget - totalSpend
        
        return HttpResponse(render(request, 'ocaccounts/dashboard.html', {
            'safespend' : remainingBudget.quantize(Decimal('0'), rounding=ROUND_UP), 
            'totalbalance' : totalbalance,
            'form' : UploadFileForm(),
        }))
