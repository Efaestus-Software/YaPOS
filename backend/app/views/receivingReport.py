from django.http.response import JsonResponse, HttpResponseForbidden
from rest_framework.decorators import permission_classes
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from decimal import Decimal

class ReceivingReportAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        object = ReceivingReport.objects.all().order_by('-pk')
        s = ReceivingReportSZ(object, many=True)
        return JsonResponse(s.data, safe=False)

    def post(self, request):
        if not request.user.is_superuser:
            # trigger error 401
            return HttpResponseForbidden()
        data = request.data
        rr = ReceivingReport()
        rr.suppliers = Suppliers.objects.get(pk=data['suppliers'])
        rr.date = data['date']
        rr.code = data['code']
        rr.amountTotal = Decimal(data['amountTotal'])
        rr.createdBy = request.user

        rr.save()

        for item in data['items']:
            rri = ReceivingReportItems()
            rri.rr = rr
            rri.inventory = Inventory.objects.get(pk=item['inventory'])
            rri.remaining = item['remaining']
            rri.unitCost = Decimal(item['unitCost'])
            rri.amountTotal = Decimal(item['amountTotal'])
            rri.qty = item['qty']

            rri.inventory.qty += rri.qty

            rri.inventory.save()
            rri.save()

        return JsonResponse(0, safe=False)

        