from django.db.models import Model, CharField, BooleanField, DecimalField, PROTECT, ForeignKey, DateField, TextField, Sum
from django.template.defaultfilters import default
from polymorphic.models import PolymorphicModel
from django.db.models.query_utils import Q
from datetime import datetime
from decimal import Decimal

# Just a set of related invoices
class Project(Model):
    name = CharField(max_length=255)
    def __str__(self):
        return self.name

class Category(Model):
    class Meta:
        verbose_name_plural = 'Categories'

    BUDGET_PERIODS = (
        ('L', 'Lifetime'),
        ('Y', 'Yearly'),
        ('M', 'Monthly'),
        ('W', 'Weekly'),
        ('D', 'Daily')
    )

    PERIOD_FILTERS = (
        ('L', lambda self: (self.charge_set.instance_of(Charge))),
        ('Y', lambda self: (self.charge_set.instance_of(Charge).filter(dateMade__year=datetime.now().year))),
        ('M', lambda self: (self.charge_set.instance_of(Charge).filter(dateMade__month=datetime.now().month))),
        ('W', lambda self: (self.charge_set.instance_of(Charge).filter(dateMade__week=datetime.now().isocalendar()[1]))),
        ('D', lambda self: (self.charge_set.instance_of(Charge).filter(dateMade__year=datetime.now().year))),
    )

    name = CharField(max_length=255)
    budget = DecimalField(max_digits=10, decimal_places=2)
    budgetPeriod = CharField(max_length=1, choices=BUDGET_PERIODS)

    def getSpend(self, period=''):
        period = self.budgetPeriod if (period == '') else period
        total = dict(self.PERIOD_FILTERS)[period](self).aggregate(Sum('quantity'))['quantity__sum']

        return total if total is not None else 0

    def remainingBudget(self, period=''):
        period = self.budgetPeriod if (period == '') else period
        budget = self.scaleBudget(period)
        spend = self.getSpend(period)

        return budget - spend

    def scaleBudget(self, period):
        budget = self.budget

        if(period == self.budgetPeriod):
            return budget

        period = self.budgetPeriod if (period == '') else period
        if (budget == period): return budget
        if (period == 'L' or self.budgetPeriod == 'L'): return 0
        # Lifetime can't be scaled to anything else for infinity reasons

        if(self.budgetPeriod == 'M'): budget = budget * Decimal('12.00')
        if(self.budgetPeriod == 'W'): budget = budget * Decimal('52.00')
        if(self.budgetPeriod == 'D'): budget = budget * Decimal('365.00')

        if(period == 'M'): budget = budget / Decimal('12.00')
        if(period == 'W'): budget = budget / Decimal('52.00')
        if(period == 'D'): budget = budget / Decimal('365.00')

        # Caveat - obviously this returns an average
        return budget

    def spendPercent(self, period=''):
        period = self.budgetPeriod if (period == '') else period

        return (self.getSpend(period) / self.scaleBudget(period)) * 100

    def spendPercentCapped(self, period=''):
        pc = self.spendPercent(period)

        return pc if (pc < 100) else 100

    def __str__(self):
        return self.name

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

# Glorified collection of charges and transactions
# Not all charges and payments need to have one - can do charges and payments against account
# Relation is for convenience - account balance takes precedence
class Invoice(Model):
    dateRaised = DateField('Date Issued')
    project = ForeignKey(Project, on_delete=PROTECT, null=True, blank=True)
    issuer = ForeignKey(Entity, on_delete=PROTECT)
    def __str__(self):
        return self.issuer.name + ' - ' + self.date.strftime('%B %d, %Y')

# Unipolar, always registers a deducation from balance with payee
# Someone charging us for something
class Charge(PolymorphicModel):
    description = TextField(max_length=1000, blank=True)
    quantity = DecimalField(max_digits=12, decimal_places=2)
    category = ForeignKey(Category, on_delete=PROTECT, blank=True, null=True)

    # Always where the value is debited from
    source = ForeignKey(Entity, on_delete=PROTECT, related_name='source_set')
    dateMade = DateField('Date Made')
    invoice = ForeignKey(Invoice, on_delete=PROTECT, blank=True, null=True)

    gift = BooleanField(default=False)

    def __str__(self):
        return (self.description[:77] + '..') if len(self.description) > 80 else self.description

# Bipolar, credits the payee and debits the source
# Us paying things and internal transfers
class Transaction(Charge):
    # Where the value is credited
    sink = ForeignKey(Entity, on_delete=PROTECT, related_name='sink_set')
    category = None
