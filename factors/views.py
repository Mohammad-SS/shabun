from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import View
from factors import models
from django.http import JsonResponse


# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, "adminpanel/home.html")


# class ShowAllItems(View):
#     def get(self , request):
#         items = models.Item.objects.all()
#         return HttpResponse(items.name)

class ShowAllFactors(View):
    def get(self, request):
        factors = models.Factor.objects.all()
        return render(request , "adminpanel/archive.html" )


class CreateNewFactorItems(View):
    def get(self, request):
        items = models.Item.objects.all()
        return render(request, "factors/newfactor.html", {"items": items})


class CreateNewFactorPrices(View):
    def post(self, request):
        clientName = request.POST['client']
        sku = request.POST['sku']
        factorName = request.POST['name']
        itemsList = list(map(int, request.POST.getlist('items')))
        items = models.Item.objects.filter(pk__in=itemsList)
        return render(request, "factors/newfactorprices.html",
                      {"items": items, "factorName": factorName, "sku": sku, "clientname": clientName})

class CreateNewFactor(View):
    def post(self, request):
        clientName = request.POST['client']
        sku = request.POST['sku']
        factorName = request.POST['name']
        itemsList = list(map(int, request.POST.getlist('items')))
        items = models.Item.objects.filter(pk__in=itemsList)
        return render(request, "factors/newfactorprices.html",
                      {"items": items, "factorName": factorName, "sku": sku, "clientname": clientName})


class ShowFactorDetails(View):
    def get(self, request, pk):
        factor = get_object_or_404(models.Factor, pk=pk)
        return render(request, "factors/factorDetails.html", {"factor": factor})

    def post(self, request):
        factors = models.Factor.objects.all()
        return HttpResponse(factors)
