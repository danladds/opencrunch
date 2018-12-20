from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse_lazy
from ocaccounts.models.fundamentals import Entity
import csv
from ocaccounts.forms.charges import UploadFileForm
from io import StringIO
import json
from decimal import Decimal

class Entities(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse(render(request, 'ocaccounts/entities.html', {
            'favs' : Entity.objects.filter(fav=True).order_by('name'),
            'creditors' : Entity.objects.filter(balance__lt=0.00, fav=False).order_by('name'),
            'debtors' : Entity.objects.filter(balance__gt=0.00, fav=False).order_by('name'),
            'all' : Entity.objects.all().order_by('name'),
        }))
        
class EntitiesDump(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse(render(request, 'ocaccounts/entities-dump.html', {
            'all' : Entity.objects.all().order_by('name'),
            'form' : UploadFileForm(),
        }))
        
class EntitiesDumpCSV(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="entities.csv"'
        writer = csv.writer(response)
        
        for entity in Entity.objects.all().order_by('name'):
            writer.writerow([entity.icon, entity.name, entity.fav, entity.balance, entity.openingBal])
            
        return response

class EntitiesImportCSV(LoginRequiredMixin, View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        data = ''
        out = 'Done: '
        
        if form.is_valid():
            
            data = request.FILES['importFile'].read()
            f = StringIO(data.decode('utf-8'))
            reader = csv.reader(f)
        
            for row in reader:
                
                entity = Entity()
                entity.icon = row[0]
                entity.name = row[1]
                entity.fav = row[2]
                entity.balance = row[3]
                entity.openingBal = row[4]
                
                entity.save()
                out = out + '({0}), '.format(entity.id)
        else: out = json.dumps(form.errors, indent=1)
            
        return HttpResponse(out)
    
    
