from django.http import HttpResponseForbidden
from django.http.response import JsonResponse
from rest_framework.decorators import permission_classes
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from decimal import Decimal
import pandas as pd
import json

class CustomersAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        object = Customers.objects.all().order_by('name')
        s = CustomerSZ(object, many=True)
        return JsonResponse(s.data, safe=False)

    def post(self, request):
        if not request.user.is_superuser:
            # trigger error 401
            return HttpResponseForbidden()
        data = request.data
        s = Customers()
        s.name = data['name']
        s.address = data['address']
        s.contact = data['contact']
        s.email = data['email']
        s.save()
        return JsonResponse(s.id, safe=False)

class CustomerDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        object = Customers.objects.get(pk=pk)
        s = CustomerSZ(object)
        return JsonResponse(s.data, safe=False)

    def put(self, request, pk):
        if not request.user.is_superuser:
            # trigger error 401
            return HttpResponseForbidden()
        data = request.data
        s = Customers.objects.get(pk=pk)
        s.name = data['name']
        s.address = data['address']
        s.contact = data['contact']
        s.email = data['email']
        s.save()
        return JsonResponse(s.pk, safe=False)

    def delete(self, request, pk):
        if not request.user.is_superuser:
            # trigger error 401
            return HttpResponseForbidden()
        s = Customers.objects.get(pk=pk)
        s.delete()
        return JsonResponse(s.pk, safe=False)

class ImportCustomerExcelAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self, request):
        data = request.data
        df = pd.read_excel(data['file'])
        jsonDF = json.loads(df.to_json(orient='records'))
        for i in jsonDF:
            if Customers.objects.filter(name=i['Name']).exists():
                continue 
            s = Customers()
            s.name = i['Name']
            s.address = i['Address']
            s.contact = i['Contact']
            s.email = i['Email']
            s.save()
        return JsonResponse(0, safe=False)