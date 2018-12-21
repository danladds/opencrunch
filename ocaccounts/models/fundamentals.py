from django.db.models import Model, CharField, BooleanField, DecimalField, PROTECT, ForeignKey, DateField, TextField, Sum
from django.template.defaultfilters import default
from polymorphic.models import PolymorphicModel
from django.db.models.query_utils import Q
from datetime import datetime
from decimal import Decimal
from .entity import Entity

# Just a set of related invoices
class Project(Model):
    name = CharField(max_length=255)
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

    
    
