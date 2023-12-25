from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
 
from .models import Vendor,MyUser,PurchaseOrder
from .serializers import VendorSerializer,PurchaseOrderSerializer



from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from django.core.exceptions import ValidationError




import datetime


class HomeAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # THIS METHOD IS TO GET THE LIST OF ALL VENDORS SORTED BY NAME
    def get(self, request):
        try:
            obj = Vendor.objects.all().order_by("name")
        except Vendor.EmptyResultSet:
            return Response({"status":"error",
                                "details":"No record found."},status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(obj, many= True)
        return Response(serializer.data)
    
    
    # THIS METHOD IS TO CREATER A NEW RECORD OF VENDOR
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success',
                                    "details":"Successfully saved!",
                                    "data":serializer.data
                                    },
                                    status=status.HTTP_200_OK )
        else:
            return Response({'status': 'error',
                                "details":serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
            
            
            
class DetailVendorAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    #  THIS METHOD IS TO GET THE DETAIL INFO OF ONE VENDOR
    def get (self, request , vendor_id):
        try:
            obj =  Vendor.objects.get(vendor_code=vendor_id)
        except (ValidationError, ValueError, Vendor.DoesNotExist) as E:
            
            return Response({"status":"error",
                                "details":"No record found! please provide a valid id."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(obj)
        return Response(serializer.data)
    
    
    #  THIS METHOD IS TO UPDATE THE DETIALS OF ONE VENDOR FROM ADMIN SIDE
    def put(self,request,vendor_id):
        try:
            obj = Vendor.objects.get(vendor_code=vendor_id)
        except (Vendor.DoesNotExist):
            return Response({"status":"error",
                             "details":"Vendor record not found."},status=status.HTTP_404_NOT_FOUND)
        except (ValidationError, ValueError) as E:
            
            return Response({"status":"error",
                                "details":"No record found! please provide a valid id."},
                            status=status.HTTP_404_NOT_FOUND)
        #  THIS CONDITION IS TO CHECK WHETHER THE user is super user that can change record for vendor
        if not request.user.is_superuser:
            return Response({"status":"error",
                             "details":"You are not allowed to update vendor record."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = VendorSerializer(obj, data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success","details":"successfully updated"
                             ,"data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    # THIS METHOD IS TO DELETE THE VENDOR RECORD
    def delete(self,request,vendor_id):
        try:
            obj = Vendor.objects.get(vendor_code=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"status":"error",
                             "details":"Venor not found."},status=status.HTTP_404_NOT_FOUND)
        if not request.user.is_superuser:
            return Response({"status":"error",
                             "details":"You dont have permission to delete vendor records!"},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response({"status":"success",
                         "details":"successfully deleted post."})
        
        
        
class PurchaseOrderAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # THIS METHOD IS TO GET ALL THE DETAILS OF PO
    def get (self, request):
        try:
            obj = PurchaseOrder.objects.all().order_by("-order_date")
        except PurchaseOrder.EmptyResultSet:
            return Response({"status":"error",
                                "details":"No record found."},status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(obj, many= True)
        return Response(serializer.data)
    
    
    # THIS METHOD IS TO CREATE A NEW PO
    def post(self, request):
        try:      
            vendorid = request.data['vendor_id'] if request.data['vendor_id'] != "" else False     
        except Exception as E:
            return Response({"status":"error "
                                ,"details":"please provide the valid vendor id argument."
                                ,"data":"serializer.data"}
                                ,status=status.HTTP_400_BAD_REQUEST)
        
        try:
            
            current_date = datetime.datetime.now() 
            
            obj= PurchaseOrder.objects.create(order_date=current_date,
                vendor =  Vendor.objects.get(vendor_code=vendorid),                              
                customer=MyUser.objects.get(email= request.user.email),
               )
    
            serializer=  PurchaseOrderSerializer(obj)
            # return Response(serializer.data)
            return Response({"status":"success","details":"successfully updated"
                             ,"data":serializer.data},status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({"status":"error "
                             ,"details":"vendor not found. please provide the valid vendor id."
                             ,"data":""}
                            ,status=status.HTTP_400_BAD_REQUEST)
        except MyUser.DoesNotExist:
            return Response({"status":"error "
                             ,"details":"User not found. please provide the valid user credentials."
                             ,"data":""}
                            ,status=status.HTTP_400_BAD_REQUEST)
            
        except ValidationError as E:
          
            return Response({"status":"error "
                             ,"details":"provide valid id for vendor."
                             ,"data":""}
                            ,status=status.HTTP_400_BAD_REQUEST)


class DetailPurchaseOrderAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    
    def get (self, request, PO_NO):
        try :
            obj=  PurchaseOrder.objects.get(po_number= PO_NO)
            
            serializer = PurchaseOrderSerializer(obj)
            return Response(serializer.data)
        except ValidationError:
            return Response({"status":"error "
                             ,"details":"provide the valid PO number."
                             ,"data":""}
                            ,status=status.HTTP_400_BAD_REQUEST) 
        except PurchaseOrder.DoesNotExist:
            return Response({"status":"error",
                                "details":"PO not found."},status=status.HTTP_404_NOT_FOUND)
            
    def put(self, request, PO_NO):
        try:
            obj = PurchaseOrder.objects.get(po_number=PO_NO)
        except (PurchaseOrder.DoesNotExist):
            return Response({"status":"error",
                             "details":"PO record not found."},status=status.HTTP_404_NOT_FOUND)
        except (ValidationError) as E:
            return Response({"status":"error",
                            "details":"please provide a valid po number."},
                            status=status.HTTP_404_NOT_FOUND)
            
        serializer = PurchaseOrderSerializer(obj, data=request.data)

        if serializer.is_valid():
            
            serializer.save(customer = MyUser.objects.get(email=request.user.email))
            return Response({"status":"success","details":"successfully updated"
                             ,"data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

            