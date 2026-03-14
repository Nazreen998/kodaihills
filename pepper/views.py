from django.shortcuts import render,redirect
from .models import Data,Cart,Order,Profile
import razorpay
import uuid
from django.conf import settings

def product(request):
    a = Data.objects.all()
    return render(request,'index.html',{'a':a})

def add_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect('/login')

    item_product = Data.objects.get(id=product_id)

    cart_item = Cart.objects.filter(
        user=request.user,
        product=item_product
    ).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(
            user=request.user,
            product=item_product,
            quantity=1
        )

    return redirect('/cart')

def view_cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.amount * item.quantity

    return render(request,'cart.html',{
        'cart':cart_items,
        'total':total
    })

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    cart_items = Cart.objects.filter(user=request.user)

    subtotal = 0
    for item in cart_items:
        subtotal += item.product.amount * item.quantity

    shipping = 0
    if subtotal < 500:
        shipping = 50

    total = subtotal + shipping

    if request.method == "POST":

        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        pincode = request.POST['pincode']
        district = request.POST['district']
        payment = request.POST['payment']

        order_id = str(uuid.uuid4())

        if payment == "cod":

            Order.objects.create(
                order_id=order_id,
                name=name,
                phone=phone,
                email=email,
                address=address,
                pincode=pincode,
                district=district,
                payment_method="COD",
                total_amount=total
            )

            Cart.objects.filter(user=request.user).delete()

            return redirect('/order-success')


        if payment == "upi":

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

            payment_order = client.order.create({
                "amount": total*100,
                "currency":"INR",
                "payment_capture":"1"
            })

            Order.objects.create(
                order_id=order_id,
                name=name,
                phone=phone,
                email=email,
                address=address,
                pincode=pincode,
                district=district,
                payment_method="UPI",
                total_amount=total
            )

            return render(request,"payment.html",{
                "payment":payment_order,
                "total":total,
                "key": settings.RAZORPAY_KEY_ID
            })

    profile = None

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    return render(request, 'checkout.html', {
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'profile': profile
    })

def remove_cart(request,cart_id):
    item = Cart.objects.get(id=cart_id,user=request.user)
    item.delete()
    return redirect('/cart')

def increase_qty(request,cart_id):
    item = Cart.objects.get(id=cart_id,user=request.user)
    item.quantity += 1
    item.save()
    return redirect('/cart')

def decrease_qty(request,cart_id):
    item = Cart.objects.get(id=cart_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect('/cart')

def order_success(request):
    return render(request,'success.html')

def track_order(request):

    if request.method=="POST":

        order_id=request.POST['order_id']

        order = Order.objects.filter(order_id=order_id).first()

        return render(request,"track.html",{"order":order})

    return render(request,"track.html")

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def register(request):

    if request.method=="POST":

        username=request.POST['username']
        password=request.POST['password']
        phone=request.POST['phone']
        email=request.POST['email']
        address=request.POST['address']
        pincode=request.POST['pincode']
        district=request.POST['district']

        user=User.objects.create_user(username=username,password=password)

        Profile.objects.create(
            user=user,
            phone=phone,
            email=email,
            address=address,
            pincode=pincode,
            district=district
        )

        return redirect('/login')

    return render(request,'register.html')

def user_login(request):

    if request.method=="POST":

        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')

    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')