from django.contrib import admin
from factors import models
# Register your models here.

admin.site.register(models.Item)
admin.site.register(models.Factor)
admin.site.register(models.FactorLookUp)
