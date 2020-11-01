from django.shortcuts import render, HttpResponse, get_object_or_404 , redirect
from django.views import View
from factors import models
import uuid
import random
from xlsxwriter.workbook import Workbook
import datetime
import jdatetime
import pandas as pd
# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, "adminpanel/home.html")


class ShowAllFactors(View):
    def get(self, request):
        factors = models.Factor.objects.all()
        return render(request , "adminpanel/archive.html" ,{"factors" : factors} )

class CreateNewFactorItems(View):
    def get(self, request):
        items = models.Item.objects.all()
        return render(request, "adminpanel/newArchiveItem.html", {"items": items})


class CreateNewFactorPrices(View):
    def post(self, request):
        clientName = request.POST['client']
        if "sku" in request.POST and not request.POST['sku'] == "" :
            sku = request.POST['sku']
        else :
            rnd = random.randrange(1,34)
            sku = str(uuid.uuid4().int)[rnd:rnd+4]
            if sku[0] == "0":
                sku = str(uuid.uuid4().int)[rnd:rnd+5]
        factorName = request.POST['name']
        itemsList = list(map(int, request.POST.getlist('items')))
        items = models.Item.objects.filter(pk__in=itemsList)
        print(itemsList)
        return render(request, "adminpanel/factorPrices.html",
                      {"items": items, "factorName": factorName, "sku": sku, "clientname": clientName})

class CreateNewFactor(View):
    def post(self, request):
        totalCost = 0
        post = request.POST
        factor = models.Factor(name=post['name'] , client=post['client'] , sku=post['sku'])
        factor.save()
        for key in post.keys() :
            if(key.find("price__") == 0):
                itemid = key[7:]
                price = post["price__"+itemid]
                number = post["number__"+itemid]
                totalPrice = int(price)*int(number)
                totalCost += totalPrice
                if post["number__"+itemid] == 0:
                    continue
                item = models.Item.objects.get(pk=itemid)
                item.lastPrice = price
                item.save()
                lookup = models.FactorLookUp(item=item , factor=factor , price=price , number=number)
                lookup.save()
        factor.totalCost = totalCost
        factor.save()
        return redirect("FactorDetails" , pk=factor.id)


class ShowFactorDetails(View):
    def get(self, request, pk):
        factor = get_object_or_404(models.Factor, pk=pk)
        items = factor.factorlookup_set.all()
        return render(request, "adminpanel/editArchiveItem.html", {"factor": factor , "items" : items})

class PrintFactorToXLS(View):
    def get(self, request, pk):
        factor = get_object_or_404(models.Factor, pk=pk)
        items = factor.factorlookup_set.all()
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=factor - "+jdatetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')+".xlsx"
        # .. and pass it into the XLSXWriter
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold' : True})
        sheet = book.add_worksheet(factor.client)
        sheet.write(0, 0, 'نام فاکتور :')
        sheet.write(0,1,factor.name)
        sheet.write(0, 2, 'نام مشتری :')
        sheet.write(0,3,factor.client)
        sheet.write(0, 4, 'شماره فاکتور :')
        sheet.write(0,5,factor.sku)
        sheet.write(1, 0, ' کد :' , bold)
        sheet.write(1,1,"نام :", bold)
        sheet.write(1, 2, 'برند :', bold)
        sheet.write(1,3,"تعداد :", bold)
        sheet.write(1, 4, 'قیمت :', bold)
        sheet.write(1,5,"قیمت نهایی :", bold)
        row = 2
        for item in items:
            sheet.write(row , 0 , item.item.pk )
            sheet.write(row , 1 , item.item.name)
            sheet.write(row , 2 , item.item.brand )
            sheet.write(row , 3 , item.number )
            sheet.write(row , 4 , item.price )
            sheet.write(row , 5 , item.finalPrice )
            # sheet.set_row(row, 20, bordered)
            row += 1
        sheet.write(row,0,"مجموع :", bold)
        sheet.write(row,1,str(row-2) + " نوع تجهیزات", bold)
        sheet.write(row,3,factor.sumitem, bold)
        sheet.write(row,5,factor.totalCost, bold)
        sheet.set_column(1,1,50)
        sheet.set_column(4,5,15)


        sheet.right_to_left()
        book.close()
        return response

class ShowAllItems(View):
    def get(self, request):
        items = models.Item.objects.all()
        return render(request , "adminpanel/showTools.html" ,{"items" : items} )

class ImportItems(View):
    def get(self , request):
        return render(request , "adminpanel/importTools.html" )
    def post(self , request):
        csv = request.FILES['csv']
        if 'update' in request.POST:
            update = int(request.POST['update'])
        else :
            update = 0
        if update == 0:
            models.Item.objects.all().delete()
        data = pd.read_csv(csv)
        names = data['name']
        brands = data['brand']
        lastPrices = data['last price']
        c = 0
        dt = datetime.datetime.now()
        for name in names:
            item = models.Item(name=name , brand= brands[c] , lastPrice=lastPrices[c] , id=c+1 , addTime=dt)
            item.save()
            c = c + 1
        return redirect("ShowAllTools")