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
from ..forms.charges import UploadFileForm
from ..forms.categories import CategoryForm

class NewCategory(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = 'ocaccounts/newcategory.html'
    success_url = reverse_lazy('ocaccounts:categories')

class EditCategory(LoginRequiredMixin, UpdateView):
    form_class = CategoryForm
    model = Category
    template_name = 'ocaccounts/editcategory.html'
    success_url = reverse_lazy('ocaccounts:categories')

class Categories(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse(render(request, 'ocaccounts/categories.html', {
            'category_week': Category.objects.filter(budgetPeriod='W').order_by('name'),
            'category_month': Category.objects.filter(budgetPeriod='M').order_by('name'),
            'out_of_budget': Charge.objects.filter(Q(category=None), \
                                            Q(dateMade__month=datetime.now().month), \
                                            ~Q(instance_of=Transaction), \
                                            Q(gift=False))\
                                            .aggregate(Sum('quantity'))['quantity__sum'],
            'category_year': Category.objects.filter(budgetPeriod='Y').order_by('name'),
        }))
        
class OutOfBudget(View):
    def get(self, request):
        return HttpResponse(render(request, 'ocaccounts/outofbudget.html', {
            'charges': Charge.objects.filter(Q(category=None), \
                                            Q(dateMade__month=datetime.now().month), \
                                            ~Q(instance_of=Transaction), \
                                            Q(gift=False)).order_by('-dateMade')
        }))
        
class CategoriesDump(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse(render(request, 'ocaccounts/categories-dump.html', {
            'all' : Category.objects.all().order_by('name'),
            'form' : UploadFileForm(),
        }))
        
class CategoriesDumpCSV(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="categories.csv"'
        writer = csv.writer(response)
        
        for category in Category.objects.all().order_by('name'):
            writer.writerow([category.name, category.budget, category.budgetPeriod])
            
        return response
    
class CategoriesImportCSV(LoginRequiredMixin, View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        data = ''
        out = 'Done: '
        
        if form.is_valid():
            
            data = request.FILES['importFile'].read()
            f = StringIO(data.decode('utf-8'))
            reader = csv.reader(f)
        
            for row in reader:
                category = Category()
                
                category.name = row[0]
                category.budget = row[1]
                category.budgetPeriod = row[2]
                
                category.save()
                out = out + '({0}), '.format(category.id)
        else: out = json.dumps(form.errors, indent=1)
            
        return HttpResponse(out)
        
        
class DeleteCategory(DeleteView):
    model = Category
    success_url = reverse_lazy('ocaccounts:deletesuccess')

    def delete(self, request, *args, **kwargs):

        return super(DeleteCategory, self).delete(request, *args, **kwargs)
