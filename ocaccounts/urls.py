from django.urls import path
from ocaccounts.views import Dashboard, Entities, Categories, EntityAccount, Reports, OutOfBudget, \
    EntitiesDump
from django.urls.conf import include
from ocaccounts.views.charges import NewChargeSuccess, NewCharge, NewTransaction,\
    DeleteSuccess, DeleteCharge, ImportStatement, NewTransactionSuccess,\
    ChargesDump, ChargesDumpCSV, ChargesImportCSV, ChargesList, ChargesImportCajamarCSV, \
    ChargesImportCajamarCSVSave
from ocaccounts.views.categories import CategoriesDump, CategoriesDumpCSV,\
    CategoriesImportCSV, NewCategory, DeleteCategory, EditCategory, MonthlyReport
from ocaccounts.views.entities import EntitiesDumpCSV, EntitiesImportCSV

app_name = 'ocaccounts'

urlpatterns = [
    path('authentication/', include('django.contrib.auth.urls')),
    path('', Dashboard.as_view(), name='dashboard'),
    path('reports/', Reports.as_view(), name='reports'),
    path('reports/monthly/<int:index>/', MonthlyReport.as_view(), name='monthlyreport'),
    path('statement/import/', ChargesImportCajamarCSV.as_view(), name='importstatement'),
    path('statement/import/save/', ChargesImportCajamarCSVSave.as_view(), name='importstatementsave'),

    path('balances/', Entities.as_view(), name='entities'),
    path('balance/<int:pk>/', EntityAccount.as_view(), name='balance'),
    path('entities/dump/', EntitiesDump.as_view(), name='entitiesdump'),
    path('entities/dump/csv/', EntitiesDumpCSV.as_view(), name='entitiesdumpcsv'),
    path('entities/import/csv/', EntitiesImportCSV.as_view(), name="entitiesimportcsv"),

    path('categories/', Categories.as_view(), name='categories'),
    path('category/new/', NewCategory.as_view(), name='newcategory'),
    path('category/<int:pk>/edit/', EditCategory.as_view(), name='editcategory'),
    path('categories/dump/', CategoriesDump.as_view(), name='categoriesdump'),
    path('categories/dump/csv/', CategoriesDumpCSV.as_view(), name='categoriesdumpcsv'),
    path('out-of-budget/', OutOfBudget.as_view(), name='outofbudget'),
    path('categories/import/csv/', CategoriesImportCSV.as_view(), name="categoriesimportcsv"),
    path('category/<int:pk>/delete/', DeleteCategory.as_view(), name='deletecategory'),

    path('purchase/new/', NewCharge.as_view(), name='newpurchase'),
    path('purchase/new/success/<int:pk>/', NewChargeSuccess.as_view(), name='newpurchasesuccess'),
    path('charge/<int:pk>/delete/', DeleteCharge.as_view(), name='deletecharge'),
    path('charge/delete/success/', DeleteSuccess.as_view(), name='deletesuccess'),
    path('payment/new/', NewTransaction.as_view(), name='newpayment'),
    path('payment/new/success/<int:pk>/', NewTransactionSuccess.as_view(), name='newpaymentsuccess'),
    path('charges/dump/', ChargesDump.as_view(), name='chargesdump'),
    path('charges/list/', ChargesList.as_view(), name='chargeslist'),
    path('charges/import/csv/', ChargesImportCSV.as_view(), name="chargesimportcsv"),
    path('charges/dump/csv/', ChargesDumpCSV.as_view(), name='chargesdumpcsv'),

]
