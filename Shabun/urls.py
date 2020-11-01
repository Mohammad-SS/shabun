"""Shabun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from factors import views as FactorsView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , FactorsView.Index.as_view() , name="home"),
    # factor paths :
    path("factors" , FactorsView.ShowAllFactors.as_view() , name="FactorsPage"),
    path("factors/new", FactorsView.CreateNewFactorItems.as_view(), name="NewFactor"),
    path("factors/new/setprices", FactorsView.CreateNewFactorPrices.as_view(), name="NewFactorPrices"),
    path("factors/new/lastStep", FactorsView.CreateNewFactor.as_view(), name="LastPriceStep"),
    path("factors/<int:pk>", FactorsView.ShowFactorDetails.as_view(), name="FactorDetails"),
    path("factors/<int:pk>/print", FactorsView.PrintFactorToXLS.as_view(), name="FactorPrinter"),

    # tools path :
    path("tools", FactorsView.ShowAllItems.as_view(), name="ShowAllTools"),
    path("tools/import", FactorsView.ImportItems.as_view(), name="ImportTools"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
