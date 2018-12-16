from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse_lazy
from ocaccounts.models.fundamentals import Category

class Categories(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse(render(request, 'ocaccounts/categories.html', {
            'category_week': Category.objects.filter(budgetPeriod='W').order_by('name'),
            'category_month': Category.objects.filter(budgetPeriod='M').order_by('name'),
            'category_year': Category.objects.filter(budgetPeriod='Y').order_by('name'),
        }))