from datetime import datetime
from decimal import Decimal

from django.db.models import Model, CharField, BooleanField, \
    DecimalField, PROTECT, ForeignKey, DateField, TextField, Sum
from polymorphic.models import PolymorphicModel
from django.db.models.query_utils import Q

from .entity import Entity
from .fundamentals import Invoice
from .category import Category

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
