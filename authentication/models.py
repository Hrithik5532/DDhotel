from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime  # Import the datetime module
from Product.models import Product

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    
    def __str__(self):
        return str(self.username)


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    first_name = models.CharField(max_length=40,null=True,blank=True)
    last_name = models.CharField(max_length=40,null=True,blank=True)
    address_line_1 = models.CharField(max_length=400)
    address_line_2 = models.CharField(max_length=400, null=True, blank=True)
    city = models.CharField(max_length=400)
    postal_code = models.CharField(max_length=400)
    mobile = models.CharField(max_length=15,null=True,blank=True)
    state = models.CharField(max_length=400)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Newsletter(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)



class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    total_price =models.CharField(max_length=400,null=True,blank=True)


    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'product')




class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    price = models.CharField(max_length=400,null=True,blank=True)
    discount_price = models.FloatField(null=True,blank=True,default=0)
    
    total = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)




class Order(models.Model):
    orderId = models.CharField(max_length=10, unique=True, blank=True, null=True)

    
    customer_first_name = models.CharField(max_length=400,null=True, blank=True)
    customer_last_name = models.CharField(max_length=400,null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    customer_contact = models.CharField(max_length=15,null=True, blank=True)
    address_line_1 = models.CharField(max_length=400)
    address_line_2 = models.CharField(max_length=400, null=True, blank=True)
    city = models.CharField(max_length=400, null=True, blank=True)
    state = models.CharField(max_length=400, null=True, blank=True)
    postal_code = models.CharField(max_length=400)

    
    order_items = models.ManyToManyField(OrderItem)
    payment_status_choices = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Cash On Delivery', 'Cash On Delivery'),
    )
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default='Pending')
    payment_id = models.CharField(max_length=50, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)  

    
    sub_total = models.FloatField(default=0)
    tax_percentage = models.FloatField(default=0)
    tax = models.DecimalField(max_digits=1000000,decimal_places=2,null=True, blank=True)

    discount_percentage = models.DecimalField(max_digits=1000000,decimal_places=2,null=True, blank=True)  
    discount_amount = models.DecimalField(max_digits=1000000,decimal_places=2,null=True, blank=True)  

    deliveryCharges = models.IntegerField(validators=[MinValueValidator(0)],null=True, blank=True)
    
    total = models.FloatField(default=0)

    

    def __str__(self):
        return str(self.payment_status) + '  '+str(self.id) + '  ' + str(self.payment_amount)
    
    