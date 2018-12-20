from django.urls import path
from ocaccounts.views import Dashboard, Entities, Categories, EntityAccount, Reports, OutOfBudget, \
    EntitiesDump
from django.urls.conf import include
from ocaccounts.views.charges import NewChargeSuccess, NewCharge, NewTransaction,\
    DeleteSuccess, DeleteCharge, ImportStatement, NewTransactionSuccess,\
    ChargesDump, ChargesDumpCSV, ChargesImportCSV
from ocaccounts.views.categories import CategoriesDump, CategoriesDumpCSV,\
    CategoriesImportCSV
from ocaccounts.views.entities import EntitiesDumpCSV, EntitiesImportCSV

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
    path('payment/new/', NewTransaction.as_view(), name='newpayment'),
    path('payment/new/success/<int:pk>/', NewTransactionSuccess.as_view(), name='newpaymentsuccess'),
    path('statement/import/', ImportStatement.as_view(), name='importstatement'),
    path('charge/delete/<int:pk>/', DeleteCharge.as_view(), name='deletecharge'),
    path('charge/delete/success/', DeleteSuccess.as_view(), name='deletesuccess'),
    path('authentication/', include('django.contrib.auth.urls')),
    path('entities/dump/', EntitiesDump.as_view(), name='entitiesdump'),
    path('categories/dump/', CategoriesDump.as_view(), name='categoriesdump'),
    path('charges/dump/', ChargesDump.as_view(), name='chargesdump'),
    path('categories/dump/csv/', CategoriesDumpCSV.as_view(), name='categoriesdumpcsv'),
    path('charges/dump/csv/', ChargesDumpCSV.as_view(), name='chargesdumpcsv'),
    path('entities/dump/csv/', EntitiesDumpCSV.as_view(), name='entitiesdumpcsv'),
    path('entities/import/csv/', EntitiesImportCSV.as_view(), name="entitiesimportcsv"),
    path('charges/import/csv/', ChargesImportCSV.as_view(), name="chargesimportcsv"),
    path('categories/import/csv/', CategoriesImportCSV.as_view(), name="categoriesimportcsv"),
]