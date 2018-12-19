from django.urls import path
from ocaccounts.views import Dashboard, Entities, Categories, EntityAccount, Reports, OutOfBudget
from django.urls.conf import include
from ocaccounts.views.charges import NewChargeSuccess, NewCharge, NewTransaction,\
    DeleteSuccess, DeleteCharge, ImportStatement

app_name = 'ocaccounts'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('balances/', Entities.as_view(), name='entities'),
    path('categories/', Categories.as_view(), name='categories'),
    path('out-of-budget/', OutOfBudget.as_view(), name='outofbudget'),
    path('balance/<int:pk>/', EntityAccount.as_view(), name='balance'),
    path('reports/', Reports.as_view(), name='reports'),
    path('purchase/new/', NewCharge.as_view(), name='newpurchase'),
    path('purchase/new/success/<int:pk>/', NewChargeSuccess.as_view(), name='newpurchasesuccess'),
    path('statement/import/', ImportStatement.as_view(), name='importstatement'),
    path('newpayment/', NewTransaction.as_view(), name='newpayment'),
    path('charge/delete/<int:pk>/', DeleteCharge.as_view(), name='deletecharge'),
    path('charge/delete/success/', DeleteSuccess.as_view(), name='deletesuccess'),
    path('authentication/', include('django.contrib.auth.urls')),
]