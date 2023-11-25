from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.home,name="home"),

    
    path('signup', views.register,name="register"),
    path('login', views.signin,name="login"),
    path('logout', views.logout_view,name="logout"),
    
    path('my-profile', views.my_profile,name="my-profile"),
    path('order-history', views.order_history,name="order_history"),
    path('add-address',views.add_address,name="add-address"),
    path('otp-verification',views.otp,name="otp"),

    #Add to Cart
    path('add-cart',views.add_cart,name='add-cart'),
    path('remove-from-cart',views.remove_from_cart,name='remove-from-cart'),
    path('my-cart',views.my_cart,name='my-cart'),

    path('update-session', views.update_session, name='update-session'),
]