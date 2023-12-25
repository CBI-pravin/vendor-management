from django.urls import path
from .views import HomeAPI, DetailVendorAPI,PurchaseOrderAPI,DetailPurchaseOrderAPI
urlpatterns = [
   
     path('vendors/',HomeAPI.as_view()),
     path('vendors/<str:vendor_id>/',DetailVendorAPI.as_view()),
     
     path('purchase_orders/',PurchaseOrderAPI.as_view()),
     path('purchase_orders/<str:PO_NO>',DetailPurchaseOrderAPI.as_view()),
]