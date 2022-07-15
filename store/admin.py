from django.contrib import admin
from .models import SiteUser,UserAddress,Product,Discount,CartItem,ProductDetailInfo,ProductCategory,ProductInventory,OrderItems,OrderDetails,ShoppingSession

# Register your models here.
admin.site.register(SiteUser)
admin.site.register(UserAddress)
admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(CartItem)
admin.site.register(ProductCategory)
admin.site.register(ProductInventory)
admin.site.register(ProductDetailInfo)
admin.site.register(OrderDetails)
admin.site.register(OrderItems)
admin.site.register(ShoppingSession)
