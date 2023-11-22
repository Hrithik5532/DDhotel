from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Newsletter)
admin.site.register(Cart)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('customer_first_name', 'customer_last_name', 'customer_email', 'customer_contact','address_line_1','address_line_2' ,'city', 'state','postal_code','order_items','payment_status','payment_id','payment_amount','sub_total','total','deliveryCharges')

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
