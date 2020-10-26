from django.db import models
import jdatetime

class Item(models.Model):
    name = models.CharField(max_length=220)
    brand = models.CharField(max_length=110)
    lastPrice = models.PositiveIntegerField()
    addTime = models.DateTimeField(auto_now_add=True)
    lastChangeTime = models.DateTimeField(auto_now=True)

    @property
    def changeTimeJalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.lastChangeTime).strftime("%Y/%m/%d")


class Factor(models.Model):
    name = models.CharField(max_length=80)
    sku = models.IntegerField()
    client = models.CharField(max_length=110)
    addTime = models.DateTimeField(auto_now=True)
    totalCost = models.IntegerField(null=True, blank=True)


class FactorLookUp(models.Model):
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    number = models.IntegerField()
    price = models.IntegerField()
