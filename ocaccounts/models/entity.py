from datetime import datetime
from decimal import Decimal

from django.db.models import Model, CharField, BooleanField, \
    DecimalField, PROTECT, ForeignKey, DateField, TextField, Sum
from django.db.models.query_utils import Q
from polymorphic.models import PolymorphicModel

class Entity(PolymorphicModel):
    class Meta:
        verbose_name_plural = 'Entities'

    ENTITY_ICONS = (
        ('person', 'Person'),
        ('shop', 'Shop'),
        ('persons', 'Club'),
        ('suitcase', 'Cash'),
        ('home', 'Bank'),
    )

    name = CharField(max_length=90)
    icon = CharField(max_length=12, default='person', choices=ENTITY_ICONS)
    fav = BooleanField(default=False)
    openingBal = DecimalField(max_digits=12, decimal_places=2)

    # Cached balance figure
    # For querying purposes only
    # Always recalculate using calcBalance()
    balance = DecimalField(max_digits=12, decimal_places=2)

    def getItems(self):
        return Charge.objects.filter(Q(source = self.id) | Q(Transaction___sink = self.id)).order_by('dateMade', 'id')

    def updateBalance(self):

        #items = self.source_set.all().order_by('-dateMade').order_by('id')

        self.getChargeList()
        self.save()

    def getChargeList(self):
        eList = []
        self.balance = self.openingBal

        eList.append({
                'quantity': self.balance,
                'date': None,
                'invoice': None,
                'description': 'Opening Balance',
                'category': 'None',
                'balance': self.balance,
            })

        for i in self.getItems():
            # If it's a transaction FROM this account
            if (isinstance(i, Transaction) and i.source == self):
                self.balance = self.balance - i.quantity
                eList.insert(0, {
                    'id': i.id,
                    'quantity': -i.quantity,
                    'date': i.dateMade.strftime('%d %b %y'),
                    'invoice': i.invoice.id if (i.invoice is not None) else 0,
                    'description': i.description + ' (to ' + i.sink.name + ')',
                    'category': i.category.name if (i.category is not None) else 'None',
                    'balance': self.balance,
                })
            elif(isinstance(i, Transaction)):
                self.balance = self.balance + i.quantity
                eList.insert(0, {
                    'id': i.id,
                    'quantity': i.quantity,
                    'date': i.dateMade.strftime('%d %b %y'),
                    'invoice': i.invoice.id if (i.invoice is not None) else 0,
                    'description': i.description + ' (from ' + i.source.name + ')',
                    'category': i.category.name if (i.category is not None) else 'None',
                    'balance': self.balance,
                })
            else:
                self.balance = self.balance - i.quantity
                eList.insert(0, {
                    'id': i.id,
                    'quantity': -i.quantity,
                    'date': i.dateMade.strftime('%d %b %y'),
                    'invoice': i.invoice.id if (i.invoice is not None) else 0,
                    'description': i.description,
                    'category': i.category.name if (i.category is not None) else 'None',
                    'balance': self.balance,
                })



        return eList

    def status(self):
        if (self.balance > 0.00): return 'C'
        elif (self.balance < 0.00): return 'D'
        else: return 'Z'

    def __str__(self):
        return self.name
