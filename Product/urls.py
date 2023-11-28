from django.urls import path
from Product import views

urlpatterns = [
   

    path("menu", views.menu, name="menu"),

    path('order-create',views.order_create,name="order-create"),


    
    path('payment/execute/',views.payment_execute,name="order-success"),
]