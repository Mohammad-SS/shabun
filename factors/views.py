from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import View
from factors import models
from django.http import JsonResponse

# Create your views here.

class Index(View):
    def get(self , request):

        return render(request, "factors/index.html")

# class ShowAllItems(View):
#     def get(self , request):
#         items = models.Item.objects.all()
#         return HttpResponse(items.name)

class ShowAllFactors(View):
    def get(self , request):
        factors = models.Factor.objects.all()
        return HttpResponse(factors)


class CreateNewFactorItems(View):
    def get(self, request):
        items = models.Item.objects.all()
        return render(request , "factors/newfactor.html" , {"items" : items})

class CreateNewFactorPrices(View):
    def post(self, request):
        itemsList = list(map(int, request.POST.getlist('items')))
        items = models.Item.objects.filter(pk__in=itemsList)
        return render(request , "factors/newfactorprices.html" , {"items" : items})

class ShowFactorDetails(View):
    def get(self, request , pk):
        factor = get_object_or_404(models.Factor,pk=pk)
        return render(request,"factors/factorDetails.html" ,{"factor":factor})

    def post(self, request):
        factors = models.Factor.objects.all()
        return HttpResponse(factors)
