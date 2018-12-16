from django.db.models import Model, CharField, BooleanField, DecimalField, PROTECT, ForeignKey, DateField, TextField
from django.template.defaultfilters import default
from polymorphic.models import PolymorphicModel

# Basic financial objects

class Entity(PolymorphicModel):
    class Meta:
        verbose_name_plural = 'Entities'
    
    name = CharField(max_length=90)
    icon = CharField(max_length=90, default='person')
    fav = BooleanField(default=False)
    openingBal = DecimalField(max_digits=12, decimal_places=2)
    
    # Cached balance figure
    # For querying purposes only
    # Always recalculate using calcBalance()
    balance = DecimalField(max_digits=12, decimal_places=2)
    
    def calcBalance(self):
        return 111.11
    
    def status(self):
        if (self.balance > 0.00): return 'C'
        elif (self.balance < 0.00): return 'D'
        else: return 'Z'
    
    def __str__(self):
        return self.name

# Just a set of related invoices
class Project(Model):
    name = CharField(max_length=255)
    def __str__(self):
        return self.name

# Glorified collection of charges and transactions
# Not all charges and payments need to have one - can do charges and payments against account
# Relation is for convenience - account balance takes precedence
class Invoice(Model):
    date = DateField('Date Issued')
    project = ForeignKey(Project, on_delete=PROTECT, null=True, blank=True)
    issuer = ForeignKey(Entity, on_delete=PROTECT)
    def __str__(self):
        return self.issuer.name + ' - ' + self.date.strftime('%B %d, %Y')

# Unipolar, always registers a deducation from balance with payee
# Someone charging us for something
class Charge(PolymorphicModel):
    description = TextField(max_length=1000)
    quantity = DecimalField(max_digits=12, decimal_places=2)
    payee = ForeignKey(Entity, on_delete=PROTECT, related_name='charges')
    date = DateField('Date')
    invoice = ForeignKey(Invoice, on_delete=PROTECT, blank=True, null=True)
    
    def __str__(self):
        return (self.description[:77] + '..') if len(self.description) > 80 else self.description
    
# Bipolar, credits the payee and debits the source
# Us paying things and internal transfers
class Transaction(Charge):
    source = ForeignKey(Entity, on_delete=PROTECT, related_name='source')

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
    
    name = CharField(max_length=255)
    budget = DecimalField(max_digits=10, decimal_places=2)
    budgetPeriod = CharField(max_length=1, choices=BUDGET_PERIODS)
    
    def __str__(self):
        return self.name
    
    