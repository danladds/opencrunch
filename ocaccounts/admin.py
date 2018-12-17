from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import Entity, Project, Invoice, Category, Transaction, Charge

# Register your models here.
admin.site.register(Entity)
admin.site.register(Project)
admin.site.register(Invoice)
admin.site.register(Category)

class ChargeChildAdmin(PolymorphicChildModelAdmin):
    base_model = Charge
    base_fieldsets = (
        (None, {
            'fields': ['dateMade', 'description', 'quantity', 'source', 'invoice'],
        }),
    )
    
class TransactionAdmin(ChargeChildAdmin):
    base_model = Transaction

class ChargeAdmin(PolymorphicParentModelAdmin):
    base_model = Charge
    child_models = (Transaction,)
    list_filter = (PolymorphicChildModelFilter,)
    
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Charge, ChargeAdmin)