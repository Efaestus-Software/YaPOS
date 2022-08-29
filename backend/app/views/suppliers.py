from django.http.response import JsonResponse, HttpResponseForbidden
from rest_framework.decorators import permission_classes
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from decimal import Decimal
import pandas as pd
import json

class SuppliersAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        object = Suppliers.objects.all().order_by('name')
        s = SuppliersSZ(object, many=True)
        return JsonResponse(s.data, safe=False)

    def post(self, request):
        if not request.user.is_superuser:
            # trigger error 401
            return HttpResponseForbidden()
        data = request.data
        s = Suppliers()
        s.name = data['name']
        s.address = data['address']
        s.contact = data['contact']
        s.email = data['email']
        s.save()
        return JsonResponse(s.id, safe=False)

class SupplierDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        object = Suppliers.objects.get(pk=pk)
        s = SuppliersSZ(object)
        return JsonResponse(s.data, safe=False)

    def put(self, request, pk):
        if not request.user.is_superuser:
            # trigger error 401
            return HttpResponseForbidden()
        data = request.data
        s = Suppliers.objects.get(pk=pk)
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
        s = Suppliers.objects.get(pk=pk)
        s.delete()
        return JsonResponse(s.pk, safe=False)

class ImportSupplierExcelAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self, request):
        data = request.data
        df = pd.read_excel(data['file'])
        jsonDF = json.loads(df.to_json(orient='records'))
        for i in jsonDF:
            if Suppliers.objects.filter(name=i['Name']).exists():
                continue 
            s = Suppliers()
            s.name = i['Name']
            s.address = i['Address']
            s.contact = i['Contact']
            s.email = i['Email']
            s.save()
        return JsonResponse(0, safe=False)