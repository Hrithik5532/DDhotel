from django.shortcuts import render,redirect
from .models import ContactUs,Reservation,Review
from django.contrib import messages
from Product.models import Product
from authentication.models import Order
# Create your views here.
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        contact = ContactUs.objects.create(name=name,email=email,phone=phone,message=message)
        contact.save()
        messages.success(request,'Submited successfully')
        return redirect('contact_us')
    
    return render(request,'contact.html')


def reservation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        persons = request.POST.get('persons')
        
        message = request.POST.get('message')
        if Reservation.objects.filter(email=email,phone=phone,date=date,time=time).exists():

            messages.error(request,f'Already Booked  With Email : {email} \n Date : {date}\n Time : {time}')
            return redirect('reservation')
        

        reservation = Reservation.objects.create(name=name,email=email,phone=phone,message=message,date=date,time=time,no_persons=persons)
        reservation.save()


        messages.success(request,'Submited successfully')
        return redirect('reservation')
    
    return render(request,'reservation.html')


def review(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        file = request.FILES['file']
        item_id = request.POST.get('item_id')
        order_id = request.POST.get('order_id')
        rating = request.POST.get('rating')
        review = Review.objects.create(name=name,email=email,phone=phone,message=message
                                       )
        
        if file:
            review.file = file
        if item_id:
            review.item = Product.objects.get(id= item_id)
        if  order_id:
            review.order = Order.objects.get(id = order_id)
        if  rating:
            review.rating = rating
        review.save()
        messages.success(request,"thank you for your Review")
        return redirect('home')
    items = Product.objects.all().distinct()
    if request.user.is_authenticated:
        orders = Order.objects.filter(customer_email = request.user.email)
    else:
        orders = []
    reviwes = Review.objects.all().distinct()[::-1]
    return render(request,'review-form.html',{'items':items,'orders':orders,'reviwes':reviwes})