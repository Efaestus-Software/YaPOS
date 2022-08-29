from unicodedata import decimal
from django.db import models
from django.db.models import Model as MM
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files import File

# Create your models here.

TYPE_OF_ADJUSTMENTS = [
    ('Spoilage', 'Spoilage'),
    ('Others', 'Others'),
]

class Customers(MM):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Customers'
        verbose_name = 'Customer'

class Suppliers(MM):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Suppliers'
        verbose_name = 'Supplier'

class TestList(MM):
    message = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name_plural = 'Test List'
        verbose_name = 'Test List'


class Category(MM):
    name = models.CharField(max_length=32)
    color = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

class Inventory(MM):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    qty = models.IntegerField(default=0)
    sellingPrice = models.DecimalField(max_digits=16, decimal_places=2)
    unitCost = models.DecimalField(max_digits=16, decimal_places=4)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name_plural = 'Inventory'
        verbose_name = 'Inventory'

    # BEFORE SAVING THE INSTANCE WE'RE REDUCING THE IMAGE
    # def save(self, *args, **kwargs):
    #     if self.image:
    #         if "images" not in self.image.url:
    #             new_image = self.reduce_image_size(self.image)
    #             self.image = new_image
    #     super().save(*args, **kwargs)
    
    def reduce_image_size(self, image):
        if image:
            img = Image.open(image)
            thumb_io = BytesIO()
            img.save(thumb_io, quality=25)
            new_image = File(thumb_io, name=image.name)
            print(image)
            return new_image
        else:
            return None

class Adjustment(MM):
    code = models.CharField(max_length=32)
    date = models.DateField(null=True)
    type = models.CharField(max_length=32, choices=TYPE_OF_ADJUSTMENTS)
    amountTotal = models.DecimalField(max_digits=16, decimal_places=4)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.code}"

    class Meta:
        verbose_name_plural = 'Adjustments'
        verbose_name = 'Adjustment'

class AdjustmentItems(MM):
    adjustment = models.ForeignKey(Adjustment, on_delete=models.CASCADE, related_name='aditems')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='aditems')
    remaining = models.IntegerField()
    unitCost = models.DecimalField(max_digits=16, decimal_places=4)
    amountTotal = models.DecimalField(max_digits=16, decimal_places=4)
    qty = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.adjustment.code} {self.inventory.code} - {self.inventory.name}"

    class Meta:
        verbose_name_plural = 'Adjustment Items'
        verbose_name = 'Adjustment Item'

class ReceivingReport(MM):
    code = models.CharField(max_length=32)
    date = models.DateField(null=True)
    amountTotal = models.DecimalField(max_digits=16, decimal_places=4)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    suppliers = models.ForeignKey(Suppliers, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.code}"

    class Meta:
        verbose_name_plural = 'Receiving Reports'
        verbose_name = 'Receiving Report'

class ReceivingReportItems(MM):
    rr = models.ForeignKey(ReceivingReport, on_delete=models.CASCADE, related_name='rritems')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='rritems')
    remaining = models.IntegerField()
    unitCost = models.DecimalField(max_digits=16, decimal_places=4)
    amountTotal = models.DecimalField(max_digits=16, decimal_places=4)
    qty = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.rr.code} {self.inventory.code} - {self.inventory.name}"

    class Meta:
        verbose_name_plural = 'Receiving Report Items'
        verbose_name = 'Receiving Report Item'

class Sales(MM):
    code = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True, null=True)
    total = models.DecimalField(max_digits=16, decimal_places=4)
    subTotal = models.DecimalField(max_digits=16, decimal_places=4)
    vat = models.DecimalField(max_digits=16, decimal_places=4)
    vatExempt = models.DecimalField(max_digits=16, decimal_places=4)
    discount = models.DecimalField(max_digits=16, decimal_places=4)
    payment = models.DecimalField(max_digits=16, decimal_places=4)
    change = models.DecimalField(max_digits=16, decimal_places=4)
    net = models.DecimalField(max_digits=16, decimal_places=4)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.SET_NULL, null=True, blank=True)
    temporaryCustomer = models.CharField(max_length=100, null=True, blank=True)
    seniorID = models.CharField(max_length=100, null=True, blank=True)
    void = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.code}"

    class Meta:
        verbose_name_plural = 'Sales'
        verbose_name = 'Sale'

class SalesItems(MM):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name='salesitems')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='salesitems')
    remaining = models.IntegerField()
    amountTotal = models.DecimalField(max_digits=16, decimal_places=4)
    qty = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.sales.code} {self.inventory.code} - {self.inventory.name}"

    class Meta:
        verbose_name_plural = 'Sales Items'
        verbose_name = 'Sales Item'

    # TO GET THE ORDER BY COUNT OF SALES ITEMS OF INVENTORY:
    # inventory.annotate(num_salesitems=Count('salesitems')).order_by('-num_salesitems')[:10]

class BusinessProfile(MM):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(null=True)
    logo = models.ImageField(upload_to='images/', null=True, blank=True)
    tin = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Business Profiles'
        verbose_name = 'Business Profile'