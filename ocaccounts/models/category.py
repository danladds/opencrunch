from datetime import datetime
from decimal import Decimal

from django.db.models import Model, CharField, BooleanField, \
    DecimalField, PROTECT, ForeignKey, DateField, TextField, Sum
from django.db.models.query_utils import Q
from polymorphic.models import PolymorphicModel

from ..models import charge

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
        ('L', lambda self: (self.charge_set.instance_of(charge.Charge))),
        ('Y', lambda self: (self.charge_set.instance_of(charge.Charge).filter(dateMade__year=datetime.now().year))),
        ('M', lambda self: (self.charge_set.instance_of(charge.Charge).filter(dateMade__month=datetime.now().month))),
        ('W', lambda self: (self.charge_set.instance_of(charge.Charge).filter(dateMade__week=datetime.now().isocalendar()[1]))),
        ('D', lambda self: (self.charge_set.instance_of(charge.Charge).filter(dateMade__year=datetime.now().year))),
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
