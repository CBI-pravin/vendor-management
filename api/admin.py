from django.contrib import admin
from .models import MyUser, Vendor, PurchaseOrder
# Register your models here.


admin.site.register(MyUser)
admin.site.register(Vendor)
admin.site.register(PurchaseOrder)