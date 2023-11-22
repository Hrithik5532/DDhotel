from django.shortcuts import render,redirect
from .models import Product,SubCategory
from authentication.models import Cart,OrderItem,Order,Address
from django.db.models import Q

# Create your views here.
def menu(request):

    

    products =  Product.objects.all()[::-1]
    if request.user.is_authenticated:
        cart_item_list = [i.product.id for i in Cart.objects.filter(user=request.user)]
    else:
        cart_item_list=[]
    
    breakfast = Product.objects.filter(category__name ='Breakfast')
    lunch = Product.objects.filter(category__name ='Lunch')
    dinner = Product.objects.filter(category__name ='Dinner')
    drinks = Product.objects.filter(category__name ='Drinks')
    subcategory = SubCategory.objects.all()
    filter_products= None
    if request.GET.get('filter')=='on':
        search = request.GET.get('search')
        veg = request.GET.get('veg')
        nonveg = request.GET.get('noneveg')
        bestSeller = request.GET.get('bestSeller')
        topRated = request.GET.get('topRated')

        if search != None:
            filter_products = Product.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search) | Q(category__name__icontains=search) | Q(subcategory__name__icontains=search)
                    ).distinct()
        else:
            filter_products =  Product.objects.all()[::-1]
        
        if veg == 'on':
            filter_products = Product.objects.filter(veg_nonveg ='Only Veg')


        if nonveg == 'on':
            filter_products = Product.objects.filter(veg_nonveg ='Only Non-Veg')

    return render(request,'menu-1.html',{'filter_products':filter_products,'subcategory':subcategory,'drinks':drinks,'dinner':dinner,'lunch':lunch,'breakfast':breakfast,'products':products,'cart_item_list':cart_item_list})


def order_create(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)
    address = Address.objects.get(user=request.user,is_default=True)
    order = Order.objects.create(
        customer_first_name = request.user.first_name,
        customer_last_name = request.user.last_name,
        customer_contact = request.user.phone,
        customer_email = request.user.email,
        address_line_1 = address.address_line_1,
        address_line_2 = address.address_line_2,
        city = address.city,
        state = address.state,
        postal_code = address.postal_code,

        payment_status= 'Pending',
    )
    sub_total = 0
    for i in cart_items:
        order_item = OrderItem.objects.create(
            product = i.product,
            quantity = i.quantity,
            total= i.total_price,
            price = i.product.price,

        )
        sub_total = float(sub_total) + float(i.total_price)
        order.order_items.add(order_item)
        order.sub_total = sub_total
        order.save()

    order.deliveryCharges = float(request.session['distance_km'])*10
    order.total = float(order.sub_total) + (float(request.session['distance_km'])*10)
    order.save()

    cart_items = Cart.objects.filter(user=request.user)
    for i in cart_items:
        i.delete()

    return redirect('order-success')


def order_success(request):

    return render(request,'order-success.html')