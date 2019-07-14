import csv
import json
from io import StringIO
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse_lazy
from django.db.models.query_utils import Q
from django.db.models.aggregates import Sum
from decimal import Decimal

from ..models import Category, Charge, Transaction, Entity

class GeneralReport(LoginRequiredMixin, View):
    def get(self, request):

        charges = Charge.objects.filter(~Q(instance_of=Transaction), Q(gift=False), Q(dateMade__range=["2018-12-01", "2019-06-30"]))

        eob_total = Charge.objects.filter(Q(category=None), \
                                            Q(dateMade__range=["2018-12-01", "2019-06-30"]), \
                                            ~Q(instance_of=Transaction), \
                                            Q(gift=False))\
                                            .aggregate(Sum('quantity'))['quantity__sum']


        return HttpResponse(render(request, 'ocaccounts/general-report.html', {
            'category_month': Category.objects.order_by('name'),
            'total_spend': round(charges.aggregate(Sum('quantity'))['quantity__sum'], 2),
            'eob_spend': round(eob_total, 2),
            'eob_pc': eob_total / Decimal('70.00'),
            'entities' : Entity.objects.all(),
        }))
