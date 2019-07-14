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

from ..models import Category, Charge, Transaction

class GeneralReport(LoginRequiredMixin, View):
    def get(self, request):

        charges = Charge.objects.filter(~Q(instance_of=Transaction), Q(gift=False))

        return HttpResponse(render(request, 'ocaccounts/general-report.html', {
            'category_month': Category.objects.order_by('name'),
            'total_spend': charges.aggregate(Sum('quantity'))['quantity__sum'],
        }))
