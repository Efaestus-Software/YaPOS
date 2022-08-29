from django.http.response import JsonResponse
from rest_framework.decorators import permission_classes
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from decimal import Decimal
from datetime import datetime, date
from django.db.models import Count

class SalesForTheMonthAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        object = Sales.objects.filter(date__month=datetime.now().month,void=False)
        
        # sum of all sales for the month
        sum = Decimal(0)
        for sale in object:
            sum += Decimal(sale.total)
        

        return JsonResponse(sum, safe=False)

class SalesForTheDayAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        object = Sales.objects.filter(date__day=datetime.now().day, void=False)
        
        # sum of all sales for the day
        sum = Decimal(0)
        for sale in object:
            sum += Decimal(sale.total)
        

        return JsonResponse(sum, safe=False)

class LowQuantityProductsAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        # get all products with quantity less than 3
        object = Inventory.objects.filter(qty__lt=3).order_by('qty')
        serializer = InventorySZ(object, many=True)
        return JsonResponse(serializer.data, safe=False)

class TopProductsAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        inventory = Inventory.objects.filter(salesitems__sales__date__month=datetime.now().month)
        x = inventory.annotate(sold=Count('salesitems')).order_by('-sold')[:10]
        serializer = InventorySpecialSZ(x, many=True)

        return JsonResponse(serializer.data, safe=False)

class SalesGraphAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        # return the sum of sales each day of the month
        object = Sales.objects.filter(date__month=datetime.now().month, void=False).order_by('date')
        # convert datetime to unix timestamp
        data = []
        data0 = []
        # if sale has same date as the previous one, add the total to the previous one
        for sale in object:
            if len(data) == 0:
                data.append([
                    (datetime(sale.date.year, sale.date.month, sale.date.day).timestamp()+28800)*1000,
                    Decimal(sale.total)
                ])
            else:
                if (datetime(sale.date.year, sale.date.month, sale.date.day).timestamp()+28800)*1000 == data[-1][0]:
                    data[-1][1] += Decimal(sale.total)
                else:
                    data.append([
                        (datetime(sale.date.year, sale.date.month, sale.date.day).timestamp()+28800)*1000,
                        Decimal(sale.total)
                    ])
        return JsonResponse({'data': data, 'name': 'Sales'}, safe=False)

class SalesGraphVoidedAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        # return the sum of sales each day of the month
        object = Sales.objects.filter(date__month=datetime.now().month, void=True).order_by('date')
        # convert datetime to unix timestamp
        data = []
        # if sale has same date as the previous one, add the total to the previous one
        for sale in object:
            if len(data) == 0:
                data.append([
                    (datetime(sale.date.year, sale.date.month, sale.date.day).timestamp()+28800)*1000,
                    Decimal(sale.total)
                ])
            else:
                if (datetime(sale.date.year, sale.date.month, sale.date.day).timestamp()+28800)*1000 == data[-1][0]:
                    data[-1][1] += Decimal(sale.total)
                else:
                    data.append([
                        (datetime(sale.date.year, sale.date.month, sale.date.day).timestamp()+28800)*1000,
                        Decimal(sale.total)
                    ])
        return JsonResponse({'data': data, 'name': 'Voided Sales'}, safe=False)
