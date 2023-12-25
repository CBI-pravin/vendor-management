
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager

# from  django.contrib.auth.models import User


import uuid 
# Create your models here.

class MyUserManager(UserManager):
    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, is_staff=True, is_superuser=True,**kwargs)
        user.set_password(password)
        user.save()
        return user







#  this model stores the data for the company 
class MyUser(AbstractUser):
    username = None
    first_name = None
    last_name=None

    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



# THIS DETAILS WILL BE FILLED BY USER ONLY 

class Vendor(models.Model):
    name = models.CharField(max_length=250)
    contact_detail = models.TextField()
    address = models.TextField()
    vendor_code =   models.UUIDField( 
         default = uuid.uuid4, 
         editable = False) 
    
    # AVERAGE RATING OF VENDOR AT THE BEGINING ARE 0.0 
    
    on_time_delivery_rate = models.FloatField(default=0.0, blank=True)
    quality_rating_avg = models.FloatField(default=0.0, blank=True)
    average_response_time = models.FloatField(default=0.0, blank=True)
    fulfillment_rate =  models.FloatField(default=0.0, blank=True)
    
    
    def __str__(self) -> str:
        return self.name
    
  
    
    
class PurchaseOrder(models.Model):
    
    STATUS_CHOICES = (
        ('pending','PENDING'),
        ('completed', 'COMPLETED'),
        ('canceled).','CANCELED'),
    )
    
    
    
    po_number =  models.UUIDField( 
         default = uuid.uuid4, 
         editable = False) 
    
    customer=  models.ForeignKey(MyUser, on_delete=models.CASCADE)
   
    vendor= models.ForeignKey(Vendor, on_delete=models.CASCADE)
    
    # ORDER DATE WILL UPDATE ONLY WHEN THE PO IS CREATED 
    order_date = models.DateTimeField(auto_now_add=True)
       
    # INITIALLY THE DELIVERY DATE IS NULL THEN AFTER CRETING PO AND ADDING THE ITEM WE CAN CREATE DATE
    # THIS DATE IS FROM THE USER SIDE WHEN HE WANTS TO HAVE 
    delivery_date = models.DateTimeField(null=True, blank=True)
    
    items =  models.JSONField(null=True, blank=True)
    
    
    #  TOTAL NUMBER OF ITEMS IN THE PO
    quantity=  models.IntegerField(null=True, blank=True)
    
    
    # STATUS OF PO  IT IS THE DELIVERY STATUS OF PO WHEN VENDOR ACKNOWLEDGE PO
    status= models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # RATING WILL BE GIVEN AFTER DELIVERY
    quality_rating = models.FloatField(null=True, blank=True)
    
    #  THIS DATE IS UPDATED WHEN ORDER IS COMPLETELY PLACED AFTER CREATING PO  
    issue_date =  models.DateTimeField(null=True, blank=True)
    
    #  THIS DATE WILL UPDATE WHEN VENDOR ACKNOWLEDGE PO
    acknowledgment_date  =  models.DateTimeField(null=True, blank=True)
    
    
    def __str__(self) -> uuid:
        return str(self.po_number)