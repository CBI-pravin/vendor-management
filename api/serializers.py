from rest_framework import serializers
from .models import Vendor, PurchaseOrder
class VendorSerializer(serializers.ModelSerializer):
    on_time_delivery_rate = serializers.IntegerField( read_only=True,)
    quality_rating_avg = serializers.IntegerField(read_only=True,)
    average_response_time = serializers.IntegerField(read_only=True,)
    fulfillment_rate = serializers.IntegerField( read_only=True,)
    class Meta:
        model = Vendor
        fields = ['id','vendor_code','name','contact_detail','address',
        'on_time_delivery_rate','quality_rating_avg', 'average_response_time', 'fulfillment_rate'
        ]
        
        
        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =PurchaseOrder
        fields = "__all__"
        
        
    