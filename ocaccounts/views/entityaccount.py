from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse_lazy
from ocaccounts.models.fundamentals import Entity
from django.http.response import JsonResponse

class EntityAccount(LoginRequiredMixin, View):
    def get(self, request, pk):
        
        entity = get_object_or_404(Entity, pk=pk)
        items = entity.charges.all().order_by('date')
        eList = []
        bal = 0
        
        for i in items:
            bal = (bal + i.quantity) if (bal != 0) else i.quantity
            
            eList.append({ 
                'quantity': i.quantity, 
                'date': i.date.strftime('%B %d, %Y'), 
                'invoice': i.invoice.id if (i.invoice is not None) else 0,
                'description': i.description,
                'balance': bal,
            })
        
        return JsonResponse({
            'items': eList,
        })