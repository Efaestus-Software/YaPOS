from django.http.response import JsonResponse, HttpResponseForbidden
from rest_framework.decorators import permission_classes
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from decimal import Decimal
import pandas as pd
import json
import pprint

class SalesAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        sales = Sales.objects.all().order_by('-pk')
        serializer = SalesSZ(sales, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = request.data

        sales = Sales()
        sales.code = data['code']
        if data['existingCustomer']:
            sales.customer = Customers.objects.get(pk=data['existingCustomer'])
        elif data['temporaryCustomer']:
            sales.temporaryCustomer = data['temporaryCustomer']

        sales.total = data['total']
        sales.subTotal = data['subTotal']
        sales.discount = data['discount']
        sales.vat = data['vat']
        sales.vatExempt = data['vatExempt']
        sales.payment = data['payInput']
        sales.change = data['change']
        sales.net = data['net']
        sales.createdBy = request.user
        try:
            sales.seniorID = data['seniorID']
        except:
            pass
        sales.save()

        for item in data['items']:
            salesItem = SalesItems()
            salesItem.sales = sales
            salesItem.inventory = Inventory.objects.get(pk=item['inventory']['id'])
            salesItem.remaining = item['inventory']['qty']
            salesItem.qty = item['qty']
            salesItem.amountTotal = item['amountTotal']
            salesItem.inventory.qty -= item['qty']

            salesItem.inventory.save()
            salesItem.save()

        return JsonResponse(sales.pk, safe=False)


class SalesDetailsAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        sales = Sales.objects.get(pk=pk)
        serializer = SalesSZ(sales, many=False)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, pk):
        if not request.user.is_superuser:
            # trigger error 401
            return HttpResponseForbidden()
        sales = Sales.objects.get(pk=pk)
        sales.delete()
        return JsonResponse(True, safe=False)


class VoidSalesAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, pk):
        # when doing void, the qty of the inventory will be increased
        sales = Sales.objects.get(pk=pk)
        # check if the sales is voided
        if not sales.void:
            for item in sales.salesitems.all():
                item.inventory.qty += item.qty
                item.inventory.save()
            # do not delete the sales, just void it
            sales.void = True
            sales.save()
            return JsonResponse(0, safe=False)
        else:
            return JsonResponse(1, safe=False)

        # RETURN CODES: 0 = success, 1 = already voided