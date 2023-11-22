from django.db import models
from Product.models import Product
from authentication.models import Order
# Create your models here.

class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email =models.EmailField()
    phone = models.CharField(max_length=13)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add =True,null=True,blank=True)

    def __str__(self):
        return self.message
    

class Reservation(models.Model):
    name = models.CharField(max_length=50)
    email =models.EmailField()
    phone = models.CharField(max_length=13)
    no_persons = models.CharField(max_length=15)
    date  =models.DateField()
    time = models.TimeField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add =True,null=True,blank=True)

    def __str__(self):
        return self.message
    
class Review(models.Model):
    name = models.CharField(max_length=50)
    email =models.EmailField()
    phone = models.CharField(max_length=13)

    file = models.FileField(upload_to='Review-files/',null=True,blank=True)
    rating = models.IntegerField(default=0)
    item = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add =True,null=True,blank=True)

    def __str__(self):
        return self.email