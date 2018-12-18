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
        entity.updateBalance()
        
        return JsonResponse({
            'balance' : entity.balance,
            'items': entity.getChargeList(),
        })