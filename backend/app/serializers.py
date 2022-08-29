from rest_framework import fields, serializers
from .models import *
from django.conf import settings

from rest_framework.serializers import ModelSerializer as MS
from django.contrib.auth.models import User

class UserSZ(MS):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'is_superuser',
            'id'
        ]

class TestListSZ(MS):
    user = UserSZ(read_only=True)
    class Meta:
        model = TestList
        fields = "__all__"

class InventorySZ(MS):
    class Meta:
        model = Inventory
        fields = "__all__"

class InventorySpecialSZ(MS):
    sold = fields.IntegerField(read_only=True)
    class Meta:
        model = Inventory
        fields = [
            'code',
            'id',
            'image',
            'name',
            'sold'
        ]

class CategorySZ(MS):
    class Meta:
        model = Category
        fields = "__all__"

# class ReceivingReportSZ(MS):
#     class Meta:
#         model = ReceivingReport
#         fields = '__all__'

# serializer for receiving report items
class ReceivingReportItemsSZ(MS):
    inventory = InventorySZ(read_only=True)
    class Meta:
        model = ReceivingReportItems
        fields = '__all__'

class SuppliersSZ(MS):
    class Meta:
        model = Suppliers
        fields = '__all__'

# serialize receiving report and its suppliers and its items and its createdBy
class ReceivingReportSZ(MS):
    suppliers = SuppliersSZ(read_only=True)
    rritems = ReceivingReportItemsSZ(read_only=True, many=True)
    createdBy = UserSZ(read_only=True)
    class Meta:
        model = ReceivingReport
        fields = '__all__'
        depth = 1

class AdjustmentItemsSZ(MS):
    inventory = InventorySZ(read_only=True)
    class Meta:
        model = AdjustmentItems
        fields = '__all__'

class AdjustmentSZ(MS):
    createdBy = UserSZ(read_only=True)
    aditems = AdjustmentItemsSZ(read_only=True, many=True)
    class Meta:
        model = Adjustment
        fields = '__all__'
        depth = 1

class CustomerSZ(MS):
    class Meta:
        model = Customers
        fields = '__all__'

class SalesItemsSZ(MS):
    inventory = InventorySZ(read_only=True)
    class Meta:
        model = SalesItems
        fields = '__all__'

class SalesSZ(MS):
    createdBy = UserSZ(read_only=True)
    customer = CustomerSZ(read_only=True)
    salesitems = SalesItemsSZ(read_only=True, many=True)
    class Meta:
        model = Sales
        fields = '__all__'
        depth = 1

class BusinessSZ(MS):
    class Meta:
        model = BusinessProfile
        fields = '__all__'