from django.http import HttpResponseForbidden
from django.http.response import JsonResponse
from rest_framework.decorators import permission_classes
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from decimal import Decimal
from datetime import date, datetime

class TestListAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        object = TestList.objects.all().order_by('-pk')

        serializer = TestListSZ(object, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = request.data
        print(request.user)
        print(data)

        testList = TestList()
        testList.message = request.data['message']
        testList.user = request.user
        testList.save()

        return JsonResponse(0, safe=False)

class LatestRRCodeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            order = ReceivingReport.objects.latest('pk')

            listed_code = order.code.split('-')
            listed_date = str(date.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'RR-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'RR-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(date.today()).split('-')
            new_code = 'RR-{}-{}-0001'.format(listed_date[0], listed_date[1])

        return JsonResponse(new_code, safe=False)

class LatestADCodeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            order = Adjustment.objects.latest('pk')

            listed_code = order.code.split('-')
            listed_date = str(date.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'AD-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'AD-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(date.today()).split('-')
            new_code = 'AD-{}-{}-0001'.format(listed_date[0], listed_date[1])

        return JsonResponse(new_code, safe=False)

class LatestSalesCodeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            order = Sales.objects.latest('pk')

            num_code = int(order.code)

            num_code += 1

            new_code = str(num_code).zfill(6)

            return JsonResponse(new_code, safe=False)
        
        except:
            return JsonResponse('000001', safe=False)

class BusinessAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        object = BusinessProfile.objects.latest('pk')

        serializer = BusinessSZ(object)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        data = request.data
        
        # check if business profile has atleast one entry using if statement
        if BusinessProfile.objects.count() == 0:
            business = BusinessProfile()
            business.name = data['name']
            business.address = data['address']
            business.contact = data['contact']
            business.website = data['website']
            business.email = data['email']
            business.tin = data['tin']
            business.save()
        else:
            business = BusinessProfile.objects.latest('pk')
            business.name = data['name']
            business.address = data['address']
            business.contact = data['contact']
            business.website = data['website']
            business.email = data['email']
            business.tin = data['tin']
            business.save()

        return JsonResponse(0, safe=False)

