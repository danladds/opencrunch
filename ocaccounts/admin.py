from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, \
    PolymorphicChildModelAdmin, PolymorphicChildModelFilter

from .models import Entity, Project, Invoice, Category

# Just registering the standard models
# Deal with charges / transactions on the frontend
admin.site.register(Entity)
admin.site.register(Project)
admin.site.register(Invoice)
admin.site.register(Category)
