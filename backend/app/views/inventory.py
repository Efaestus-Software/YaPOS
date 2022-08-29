import pandas as pd
from django.http.response import JsonResponse, HttpResponseForbidden
from rest_framework.decorators import permission_classes
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
import json

class InventoryAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        object = Inventory.objects.all().order_by('name')

        serializer = InventorySZ(object, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        # serializer = InventorySZ(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse(serializer.data, status=201)
        # return JsonResponse(serializer.errors, status=400)

        if not request.user.is_superuser:
            # trigger error 403
            return HttpResponseForbidden()
        
        print(request.data)
        for i in range(0, len(request.POST.getlist('name'))):
            inventory = Inventory()
            inventory.name = request.POST.getlist('name')[i]
            inventory.code = request.POST.getlist('code')[i]
            try:
                inventory.category = Category.objects.get(id=request.POST.getlist('category')[i])
            except:
                inventory.category = None
            inventory.sellingPrice = Decimal(request.POST.getlist('sellingPrice')[i])
            inventory.unitCost = Decimal(request.POST.getlist('unitCost')[i])
            inventory.qty = int(request.POST.getlist('qty')[i])
            try:
                inventory.image = request.FILES.getlist('image')[i]
            except:
                inventory.image = None
            inventory.save()
        return JsonResponse(0, safe=False)

class InventoryDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        object = Inventory.objects.get(pk=pk)
        serializer = InventorySZ(object)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, pk):
        if not request.user.is_superuser:
            # trigger error 403
            return HttpResponseForbidden()
        data = request.data
        inventory = Inventory.objects.get(pk=pk)
        try:
            inventory.name = data['name']
            inventory.code = data['code']
            try:
                inventory.category = Category.objects.get(pk=data['category'])
            except Exception as e:
                print(e)
                inventory.category = None
            inventory.sellingPrice = Decimal(data['sellingPrice'])
            inventory.unitCost = Decimal(data['unitCost'])
            inventory.qty = int(data['qty'])
            if data['image'] != 'null':
                inventory.image.delete()
                inventory.image = request.FILES.get('image')

            if data['imageURL'] == 'null':
                inventory.image = None

            inventory.save()
            return JsonResponse(0, safe=False)
        except Exception as e:
            return JsonResponse(e, safe=False)



    def delete(self, request, pk):
        if not request.user.is_superuser:
            # trigger error 403
            return HttpResponseForbidden()
        object = Inventory.objects.get(pk=pk)
        object.delete()
        return JsonResponse(0, safe=False)
        
class CategoriesAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        object = Category.objects.all().order_by('name')

        serializer = CategorySZ(object, many=True)

        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request):
        if not request.user.is_superuser:
            # trigger error 403
            return HttpResponseForbidden()
        serializer = CategorySZ(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class CategoryDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        object = Category.objects.get(pk=pk)
        serializer = CategorySZ(object)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, pk):
        if not request.user.is_superuser:
            # trigger error 403
            return HttpResponseForbidden()
        data = request.data
        object = Category.objects.get(pk=pk)
        serializer = CategorySZ(object, data=data)
        print(data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        if not request.user.is_superuser:
            # trigger error 403
            return HttpResponseForbidden()
        object = Category.objects.get(pk=pk)
        object.delete()
        return JsonResponse(0, safe=False)

class ImportItemsExcelAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        df = pd.read_excel(data['file'])
        jsonDF = json.loads(df.to_json(orient='records'))

        for i in jsonDF:
            if not Inventory.objects.filter(code=i['Code']).exists():
                inventory = Inventory()
                inventory.name = i['Name']
                inventory.code = i['Code']
                if i['Category']:
                    try: 
                        inventory.category = Category.objects.get(name=i['Category'])
                    except Exception as e:
                        print(e)
                        cat = Category()
                        cat.name = i['Category']
                        cat.save()
                        inventory.category = cat

                inventory.sellingPrice = Decimal(i['Selling-Price'])
                inventory.unitCost = Decimal(i['Unit-Cost'])
                inventory.qty = int(i['Quantity'])
                inventory.save()
            else:
                print('Item already exists', i['Code'])
        return JsonResponse(0, safe=False)