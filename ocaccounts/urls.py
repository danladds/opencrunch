from django.urls import path
from ocaccounts.views import Dashboard, Entities, Categories, EntityAccount, Reports, NewCharge
from django.urls.conf import include

app_name = 'ocaccounts'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('balances/', Entities.as_view(), name='entities'),
    path('categories/', Categories.as_view(), name='categories'),
    path('balance/<int:pk>/', EntityAccount.as_view(), name='balance'),
    path('reports/', Reports.as_view(), name='reports'),
    path('newpurchase', NewCharge.as_view(), name='newpurchase'),
    path('', Dashboard.as_view(), name='newpayment'),
    path('', Dashboard.as_view(), name='importstatement'),
    path('authentication/', include('django.contrib.auth.urls')),
]