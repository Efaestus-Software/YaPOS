from django.http.response import JsonResponse
from rest_framework.decorators import permission_classes
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from decimal import Decimal

class AdjustmentAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        object = Adjustment.objects.all().order_by('-pk')
        s = AdjustmentSZ(object, many=True)
        return JsonResponse(s.data, safe=False)
    
    def post(self, request):
        data = request.data
        adj = Adjustment()
        adj.code = data['code']
        adj.date = data['date']
        adj.type = data['type']
        adj.amountTotal = Decimal(data['amountTotal'])
        adj.createdBy = request.user
        adj.save()

        for item in data['items']:
            # skip if qty is zero
            if item['qty'] == 0:
                continue

            adji = AdjustmentItems()
            adji.adjustment = adj
            adji.inventory = Inventory.objects.get(pk=item['inventory'])
            adji.remaining = item['remaining']
            adji.unitCost = Decimal(item['unitCost'])
            adji.amountTotal = Decimal(item['amountTotal'])
            adji.qty = item['qty']

            # create a checker to make sure inventory.qty would go below zero
            if adji.inventory.qty < adji.qty:
                adj.delete()

                # RETURN CODE 1 IF SELLING MORE THAN INVENTORY
                return JsonResponse(1, safe=False)
            else:
                adji.inventory.qty -= adji.qty
                adji.inventory.save()
                adji.save()
        if adj.amountTotal == 0:
            adj.delete()

            # RETURN CODE 2 IF AMOUNT TOTAL IS ZERO
            return JsonResponse(2, safe=False)
            
        # RETURN CODE 0 IF SUCCESS
        return JsonResponse(0, safe=False)