from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse_lazy

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        
        safespend = 1200
        totalbalance = 3122
        
        return HttpResponse(render(request, 'ocaccounts/dashboard.html', {
            'safespend' : safespend, 
            'totalbalance' : totalbalance
        }))