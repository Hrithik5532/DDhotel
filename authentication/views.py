from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.http import JsonResponse
from geopy.distance import geodesic
import json
from geopy.geocoders import Nominatim

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random
from functions import send_email_otp

def get_lat_long(address):
    geolocator = Nominatim(user_agent="user_agent")  # Replace with your app name
    location = geolocator.geocode(address)
    
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None
# address = "16 Headingley Lane, Headingley, Leeds, LS6 2AS"
address = "Leeds LS6 1BL"
result = get_lat_long(address)

if result:
    store_latitude, store_longitude = result

store_location = (store_latitude, store_longitude)  # Replace with actual coordinates
print("!@#@@!@@@!!@#@@",store_location)



def home(request):
    return render(request,'index-4.html')



def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')

        user = authenticate(request, username=email, password=password)

        login(request, user)
        if not request.user.is_verified:
            return redirect('otp')
        
        return redirect('home')

    return render(request,"login.html",{'login':True})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        check = request.POST.get('check')
        user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,
                phone=mobile,
            )
        user.set_password(password)
        user.save()

        if check =='on':
            Newsletter.objects.create(email=email).save()

        user = authenticate(request, username=email, password=password)

        print("!!!!!!!!!!!!!!!!!!",user)
        login(request, user)
        return redirect('otp')


    return render(request,"login.html",{'register':True})

def logout_view(request):
    logout(request)
    return redirect('login')




def add_address(request):
    if request.method =='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        add_line_1 = request.POST.get('add_line_1')
        add_line_2 = request.POST.get('add_line_2')
        city= request.POST.get('city')
        state= request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        mobile = request.POST.get('mobile')

        addresses = Address.objects.filter(user=request.user,is_default=True)
        for i in addresses:
            i.is_default = False
            i.save()

        Address.objects.create(user=request.user,first_name=first_name,last_name=last_name,address_line_1=add_line_1,address_line_2=add_line_2
                               ,city=city,state=state,postal_code=zip_code,mobile=mobile,is_default=True).save()

        

    return redirect('my-cart')

def my_profile(request):
    address = Address.objects.filter(user = request.user)
    return render(request,'Profile.html',{'address':address})

def order_history(request):
    orders = Order.objects.filter(customer_email=request.user.email)[::-1]
    return render(request,'order-history.html',{'orders':orders})

def otp(request):
    if request.user.is_authenticated:
        if request.user.is_verified :
            return redirect('home')
            
    if not request.user.is_verified:

        email = request.user.email
        user = User.objects.get(email=email)
        

        if request.method == 'POST':
            otp = request.POST.get('otp')
            print("!!!!!!!!!!!!!!!",otp)
            if user.otp == otp:
                
                user.is_verified = True
                user.otp = ''
                user.save()

                request.session.pop('signup_email', None)
                messages.success(request,'Email Verified')
                return redirect('home')
                            
            else:
                messages.error(request,"OTP Invalid")
                return redirect('otp')
            
        otp = random.randint(100000, 999999)
        user.otp = otp
        user.save()
        # send opt to email
        send_email_otp(user=user,otp=otp)
        
    return render(request,'otp.html')




def add_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Login required'}, status=401)
    
    if request.GET.get('itemId'):
            id = request.GET.get('itemId')
            qty = int(request.GET.get('qty'))

            if qty == 0:
                return JsonResponse({'message': 'Error'}, status=400)

            product = Product.objects.get(id=id)
            if Cart.objects.filter(user=request.user,product=product).exists():
                cart_item = Cart.objects.get(user=request.user,product=product)
                cart_item.quantity =qty
                cart_item.total_price = float(cart_item.quantity * float(product.price))
                cart_item.save()
            else:
                cart_item = Cart.objects.create(user=request.user,product=product,quantity=int(qty),
                                                total_price =float(qty * float(product.price)) )
                cart_item.save()
            print("!!!!!!!!",'added')
            return JsonResponse({'message': 'Added successfully'})
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)

def remove_from_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Login required'}, status=400)

    if request.GET.get('itemId'):
        id = request.GET.get('itemId')

        product = Product.objects.get(id=id)
        if Cart.objects.filter(user=request.user, product=product).exists():
            cart_item = Cart.objects.get(user=request.user, product=product)
            cart_item.delete()

            return JsonResponse({'message': 'Removed'})
        else:
            return JsonResponse({'message': 'Item not found in the cart'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)





def my_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    
    user_location = request.session.get('user_location', None)

    if not user_location:
        # If not, send a request to update_session with the default addressId
        default_address = Address.objects.filter(user=request.user, is_default=True).first()
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@",default_address)
        if default_address:
            update_session(request, addressId=default_address.id)


    cart_items = Cart.objects.filter(user=request.user)
    Subtotal_price = 0

    for i in cart_items:
        Subtotal_price = float(Subtotal_price + float(i.total_price)) 
    
    addresses = Address.objects.filter(user=request.user)
    try: 
        delivery_price = float((int(request.session['distance_km'])*10))
        total_price = Subtotal_price + delivery_price
    except:
        delivery_price =None
        total_price = Subtotal_price
        
    return render(request,'my-cart.html',{'cart_items':cart_items,'addresses':addresses,'total_price':total_price,'delivery_price':delivery_price,'Subtotal_price':Subtotal_price})


def update_session(request,addressId=None):
    if request.method == 'GET':
            addressId = request.GET.get('addressId')
            if addressId != None: 
                for i in Address.objects.filter(user=request.user):
                    i.is_default = False
                    i.save()

                address = Address.objects.get(id=addressId)
                address.is_default = True
                address.save()
                full_address = f'{address.city}, {address.postal_code}'

                result = get_lat_long(full_address)

                if result:
                    user_latitude, user_longitude = result
                    user_location = (user_latitude, user_longitude)  # Replace with actual coordinates
                    distance_km = geodesic(store_location, user_location).meters

                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",full_address,"@@@",result,"-------",distance_km)
                request.session['distance_km'] = distance_km
                request.session['user_location'] = user_location  # Convert to a dictionary with x and y properties

                return redirect('my-cart')
            

