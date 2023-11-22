from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'phone', 'file', 'rating', 'item', 'order', 'message', 'created_at')

    
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')


class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'phone', 'date','no_persons','time' ,'message', 'created_at')

    

admin.site.register(Review,ReviewAdmin)
admin.site.register(ContactUs,ContactAdmin)


admin.site.register(Reservation,ReservationAdmin)
