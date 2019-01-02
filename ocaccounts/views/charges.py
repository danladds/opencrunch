import csv
import json
from io import StringIO
from decimal import Decimal
import re
from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.http.response import JsonResponse
from django.db.models.query_utils import Q
from django.core import serializers

from ..models import Entity, Charge, Transaction, Category
from ..forms import ChargeForm, TransactionForm, UploadFileForm

class NewCharge(LoginRequiredMixin, CreateView):
    form_class = ChargeForm
    template_name = 'ocaccounts/newpurchase.html'
    success_url = 'success/{id}/'
    
    def form_valid(self, form):
        response = CreateView.form_valid(self, form)
        self.object.source.updateBalance()
        return response

class NewChargeSuccess(LoginRequiredMixin, View):
    def get(self, request, pk):
        
        charge = Charge.objects.get(pk=pk)
        sources = Entity.objects.all().order_by('-fav', 'name')
        
        return HttpResponse(render(request, 'ocaccounts/newpurchasesuccess.html', {
            'charge' : charge,
            'sources': sources,
        }))
    
    def post(self, request, pk):
        sourceId = request.POST['sourceId']
        dateMade = request.POST['dateMade']
        
        charge = Charge.objects.get(pk=pk)
        payment = Transaction()
        source = Entity.objects.get(pk=sourceId)
        
        payment.dateMade = dateMade
        payment.source = source
        payment.sink = charge.source
        payment.quantity = charge.quantity
        
        payment.save()
        
        payment.source.updateBalance()
        payment.sink.updateBalance()
        
        return redirect(reverse_lazy('ocaccounts:dashboard'))

#class NewCharge(LoginRequiredMixin, View):
#    def get(self, request):
#        return HttpResponse(render(request, 'ocaccounts/newpurchase.html', {
#    }))
        
class NewTransaction(LoginRequiredMixin, CreateView):
    # Step 1 - Select person
    # Step 2 - Unpaid invoices
    # Step 3 - Manual input
    form_class = TransactionForm
    template_name = 'ocaccounts/newpayment.html'
    success_url = 'success/{id}/'
    
    def form_valid(self, form):
        response = CreateView.form_valid(self, form)
        self.object.source.updateBalance()
        self.object.sink.updateBalance()
        return response
    
class NewTransactionSuccess(LoginRequiredMixin, View):
    def get(self, request, pk):
        
        return HttpResponse(render(request, 'ocaccounts/newpaymentsuccess.html', {
        }))

class DeleteSuccess(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('Done')

class DeleteCharge(DeleteView):
    model = Charge
    success_url = reverse_lazy('ocaccounts:deletesuccess')
    
    def delete(self, request, *args, **kwargs):
        
        out = {}
        obj = Charge.objects.get(pk=kwargs['pk'])
        source = obj.source
        sink = None 
        
        if(isinstance(obj, Transaction)):
            sink = obj.sink
        
        response = super(DeleteCharge, self).delete(request, *args, **kwargs)
        
        source.updateBalance()
        out[source.id] = source.balance,
        
        if (sink is not None):
            sink.updateBalance()
            out[sink.id] = sink.balance
        
        return JsonResponse(out)

class ImportStatement(View):
    pass

class ChargesDump(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse(render(request, 'ocaccounts/charges-dump.html', {
            'all' : Charge.objects.all().order_by('-dateMade', 'id'),
            'form' : UploadFileForm(),
        }))

class ChargesList(LoginRequiredMixin, View):
    def get(self, request):
        query = Q()

        catId = int(request.GET.get('category', '0'))
        if(catId > 0): query |= Q(category=catId)


        return HttpResponse(render(request, 'ocaccounts/charges-list.html', {
            'all' : Charge.objects.filter(query).order_by('-dateMade', 'id'),
            'show_trans' : False,
            'show_gift' : False,
        }))
        
class ChargesDumpCSV(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="charges.csv"'
        writer = csv.writer(response)
        
        for charge in Charge.objects.all().order_by('-dateMade', 'id'):
            sinkName = charge.sink.name if (isinstance(charge, Transaction)) else ''
            writer.writerow([
                charge.dateMade, 
                charge.description, 
                charge.quantity, 
                charge.category.name if (charge.category is not None) else '', 
                charge.source.name,
                sinkName,
                charge.gift
            ])
            
        return response
    
class ChargesImportCSV(LoginRequiredMixin, View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        data = ''
        out = 'Done: '
        
        if form.is_valid():
            
            data = request.FILES['importFile'].read()
            f = StringIO(data.decode('utf-8'))
            reader = csv.reader(f)
            charge = None
        
            for row in reader:
                if(row[5] == ''):
                    charge = Charge()
                else:
                    charge = Transaction()
                    charge.sink = Entity.objects.filter(name=row[5]).first()
                
                charge.dateMade = row[0]
                charge.description = row[1]
                charge.quantity = row[2]
                charge.category = Category.objects.filter(name=row[3]).first()
                charge.source = Entity.objects.filter(name=row[4]).first()
                charge.gift = row[6]
                
                charge.save()
                out = out + '({0}), '.format(charge.id)
        else: out = json.dumps(form.errors, indent=1)
            
        return HttpResponse(out)

# This is going to need a lot of separating out for general and other banks
# But it's a start?
# Need to get rid of the hardcoding of account names and offer selection of accounts
class ChargesImportCajamarCSV(LoginRequiredMixin, View):

    class ImportItem:
        dateMade = None;
        description = '';
        amount = Decimal('0.00')
        tid = 0

        cardMatch = re.compile(r'OP\.TARJ\.COMPRA COMERCIO - 415007\*\*\*\*\*\*4695 ')

        def Import(self, row):
            self.dateParts = row[0].split('/')
            self.dateMade = '{2}-{1}-{0}'.format(*self.dateParts)
            self.dateObj = date(int(self.dateParts[2]), int(self.dateParts[1]), int(self.dateParts[0]))
            self.description = self.cardMatch.sub('', row[2])
            self.amount = Decimal(row[3]) * Decimal('-1')
            self.target = ''
            self.matches = []

            if('REINTEGRO' in self.description):
                self.description = 'Withdrawal'
                self.target = 'Cash'

            if('COMIS.COMPRA' in self.description):
                self.description = 'Bank Charge'
                self.target = 'Bank Charge'

            # Attempt match
            self.matches = Charge.objects.filter(Q(quantity=self.amount) & Q(dateMade=self.dateObj) &Q(source__name='Cajamar'))

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        data = ''
        out = 'Done: '

        if form.is_valid():

            data = request.FILES['importFile'].read()
            f = StringIO(data.decode('utf-8'))
            reader = csv.reader(f)
            charge = None
            idx = 0

            items = []

            for row in reader:
                item = self.ImportItem()
                item.Import(row)

                # Just skip over things that already exist for now
                # TODO: improve handing with confirmation
                if (len(item.matches) > 0):
                    continue

                item.tid = idx
                items.append(item)
                idx = idx + 1

            return HttpResponse(render(request, 'ocaccounts/importstatement.html', {
                'entities' : Entity.objects.all().order_by('name'),
                'items' : items,
                'count': idx,
            }))

        else: return HttpResponse(json.dumps(form.errors, indent=1))

class ChargesImportCajamarCSVSave(LoginRequiredMixin, View):
    def post(self, request):
        
        count = int(request.POST['count'])
        items = []

        for c in range(0, count):
            obj = Charge()
            sinkId = int(request.POST['sink_{0}'.format(c)])

            if(sinkId > 0):
                obj = Transaction()
                obj.sink = Entity.objects.get(pk=sinkId)
            elif(sinkId == -2):
                obj.gift = True

            obj.description = request.POST['description_{0}'.format(c)]
            obj.source = Entity.objects.get(pk=1)
            obj.quantity = Decimal(request.POST['amount_{0}'.format(c)])

            dateParts = request.POST['dateMade_{0}'.format(c)].split('-')
            obj.dateMade = date(int(dateParts[0]), int(dateParts[1]), int(dateParts[2]))

            items.append(obj)

        for item in items:
            item.save()

        return HttpResponse('Done')
