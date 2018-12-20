from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse_lazy
from ocaccounts.models.fundamentals import Entity, Charge, Transaction
from ..forms import ChargeForm, TransactionForm
from django.views.generic.base import TemplateView
from django.http.response import JsonResponse

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

