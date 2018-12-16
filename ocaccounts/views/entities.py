from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse_lazy
from ocaccounts.models.fundamentals import Entity

class Entities(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse(render(request, 'ocaccounts/entities.html', {
            'favs' : Entity.objects.filter(fav=True).order_by('name'),
            'creditors' : Entity.objects.filter(balance__lt=0.00, fav=False).order_by('name'),
            'debtors' : Entity.objects.filter(balance__gt=0.00, fav=False).order_by('name'),
            'all' : Entity.objects.all().order_by('name'),
        }))