from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse_lazy
from ocaccounts.models.fundamentals import Entity, Charge, Transaction
from datetime import datetime
from django.db.models.query_utils import Q
from django.db.models.aggregates import Sum

class Reports(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse(render(request, 'ocaccounts/reports.html', {
            'out_of_budget': Charge.objects.filter(Q(category=None), \
                                            Q(dateMade__month=datetime.now().month), \
                                            ~Q(instance_of=Transaction), \
                                            Q(gift=False))\
                                            .aggregate(Sum('quantity'))['quantity__sum'],
        }))