from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Entity)
admin.site.register(Project)
admin.site.register(Invoice)
admin.site.register(Charge)
admin.site.register(Transaction)
admin.site.register(Category)