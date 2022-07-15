import os.path

from django.db import models
from django.utils import timezone

# from datetime import datetime
# Create your models here.
from numpy.distutils.system_info import blas_info


class SiteUser(models.Model):
    userName = models.EmailField(
        max_length=50,
        verbose_name="User Name"
    )
    password = models.CharField(max_length=32)
    firstName = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="First Name"
    )
    lastName = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Last Name "
    )
    telephone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        verbose_name="Mobile Number"
    )
    createdAt = models.DateTimeField(default=timezone.now)
    modifyAt = models.DateTimeField(default=timezone.now)
    deletedAt = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.userName} : {self.firstName} : {self.lastName}"


class UserAddress(models.Model):
    userId = models.ForeignKey(
        SiteUser,
        verbose_name="User Name",
        on_delete=models.CASCADE
    )
    addressLine1 = models.CharField(max_length=32)
    addressLine2 = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=16)
    postelCode = models.CharField(max_length=16)
    country = models.CharField(max_length=16, blank=True)
    addressContactNumber_1 = models.CharField(
        max_length=11, null=True, blank=True)
    addressContactNumber_2 = models.CharField(
        max_length=11, null=True, blank=True)
    createdAt = models.DateTimeField(default=timezone.now)
    modifyAt = models.DateTimeField(default=timezone.now)
    deletedAt = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f" {self.id} : {self.userId.userName} : {self.userId.lastName} : {self.addressLine1} : {self.city}"


class ShoppingSession(models.Model):
    user_id = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE,
        verbose_name="User Detail"
    )
    total = models.FloatField()
    createdAt = models.DateTimeField(default=timezone.now)
    modifiedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} : {self.user_id.userName} : {self.total} : {self.createdAt}"


class ProductCategory(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name="Product Category Name"
    )
    desc = models.CharField(
        max_length=120,
        verbose_name="Category Description",
        blank=True,
        null=True
    )
    createdAt = models.DateTimeField(default=timezone.now)
    modifiedAt = models.DateTimeField(default=timezone.now)
    deletedAt = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.id} : {self.name} : {self.desc}"


class Discount(models.Model):
    name = models.CharField(max_length=32, verbose_name="Discount Offer Name")
    desc = models.CharField(
        max_length=128,
        verbose_name="Discount Description",
        blank=True,
        null=True,
    )
    discount_percent = models.FloatField()
    active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    modifiedAt = models.DateTimeField(default=timezone.now)
    deletedAt = models.DateTimeField(default=None, null=True, blank=True)

    def isActive(self):
        if self.active:
            return "Active"
        return "Not Active"

    def __str__(self):
        return f"{self.id}:{self.name}: { self.isActive() }"


class Product(models.Model):
    name = models.CharField(max_length=128)
    desc = models.CharField(
        max_length=128,
        verbose_name="Product description",
        blank=True,
        null=True,
    )
    img_url = models.ImageField(
        upload_to="images/",
        null=True,
        blank=True
    )
    category_id = models.ForeignKey(
        ProductCategory,
        verbose_name="Product Category",
        on_delete=models.SET(0)
    )
    actual_price = models.FloatField(null=True, blank=True)
    display_price = models.FloatField()
    brand = models.CharField(max_length=16, null=True, blank=True)
    discount_id = models.ForeignKey(
        Discount,
        verbose_name="Active Discount Offer",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    createdAt = models.DateTimeField(default=timezone.now)
    modifiedAt = models.DateTimeField(default=timezone.now)
    deletedAt = models.DateTimeField(default=None, null=True, blank=True)

    def isDiscountActive(self):
        if self.discount_id == None or self.discount_id:
            return f"No Discount"
        return f"Discount Available: {self.discount_id.name} : {self.discount_id.discount_percent}"

    def __str__(self):
        return f"{self.id} : {self.name} : {self.actual_price} : {self.display_price} : {self.isDiscountActive()}"


class ProductInventory(models.Model):
    product_id = models.ForeignKey(
        Product,
        verbose_name="Product",
        on_delete=models.CASCADE,
        null=True
    )
    quantity = models.PositiveIntegerField()
    createdAt = models.DateTimeField(default=timezone.now)
    modifiedAt = models.DateTimeField(default=timezone.now)
    deletedAt = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"Product Inventory : Quantity={self.quantity}"


class ProductDetailInfo(models.Model):
    productId = models.ForeignKey(
        Product,
        verbose_name="Product Id",
        on_delete=models.CASCADE
    )
    rear_Camara = models.CharField(max_length=64)
    front_camara = models.CharField(max_length=64, null=True, blank=True)
    ram = models.PositiveSmallIntegerField()
    inbuilt_storage = models.PositiveSmallIntegerField()
    expandable_storage = models.PositiveSmallIntegerField(
        null=True, blank=True)
    processor_brand = models.CharField(max_length=16, null=True, blank=True)
    operating_system = models.CharField(max_length=16)
    screen = models.CharField(max_length=16, null=True, blank=True)
    battery_power = models.FloatField()
    battery_type = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return f"{self.id} : {self.productId.name} info"


class OrderDetails(models.Model):
    user_id = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE,
        verbose_name="User Detail"
    )
    cartId = models.ForeignKey(
        ShoppingSession,
        verbose_name="Cart ID",
        null=True,
        on_delete=models.SET_NULL,
    )
    applied_offer = models.ForeignKey(
        Discount,
        verbose_name="Applied Discount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )
    total = models.FloatField()
    discount_percentage = models.FloatField(null=True, blank=True, default=0)
    discounted_price = models.FloatField(null=True, blank=True)
    createdAt = models.DateTimeField(default=timezone.now)
    modifiedAt = models.DateTimeField(default=timezone.now)

    def count_discounted_price(self):
        ans = self.total
        if self.discount_percentage != 0:
            ans = (float(self.total) * float(self.discount_percentage))/100
        return ans

    def __str__(self):
        return f"{self.id} : {self.total} : {self.discount_percentage} : {self.discounted_price}"


class OrderItems(models.Model):
    order_id = models.ForeignKey(
        OrderDetails,
        on_delete=models.CASCADE,
        verbose_name="Order Detail"
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product Name"
    )
    quantity = models.PositiveIntegerField()
    createdAt = models.DateTimeField(default=timezone.now)
    modifiedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} : Order Id = {self.order_id.id}: Product Id = {self.product_id.id}  "


class CartItem(models.Model):
    session_id = models.ForeignKey(
        ShoppingSession,
        on_delete=models.CASCADE,
        related_name="session"
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Cart Product Detail"
    )
    quantity = models.PositiveIntegerField()
    createdAt = models.DateTimeField(default=timezone.now)
    modifiedAt = models.DateTimeField(default=timezone.now, blank=True, null=True)
    deletedAt = models.DateTimeField(default=None, blank=True, null=True)

    def getTotal(self):
        return int(self.quantity) * int(self.product_id.display_price)

    def __str__(self):
        return f"{self.id} :Session Id = {self.session_id.id} : Product Id = {self.product_id.id}"
