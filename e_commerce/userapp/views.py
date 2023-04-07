from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.conf import settings
from .models import UserProfile, Address,Review
from.forms import UserProfileForm,UserForm
from adminapp.models import ProductImage,Product,Category,Banner,ProductVarient
from django.core.paginator import Paginator
from django.db.models import Q
from productapp.models import Order,OrderProduct
from django.http import JsonResponse
from django.template.loader import render_to_string
import razorpay
import e_commerce.settings


# Create your views here.
def base (request):
    banner=Banner.objects.all()
    return render(request,'user/base.html',locals())


def loginpage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'user login successfull')
            return redirect(base)
        else:
            messages.info(request,'invalid username or password')
    return render(request,'user/login.html',locals())

def register(request):
    user = None 
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if User.objects.filter(first_name=username).exists():
            messages.info(request,'user name not available ')
            return redirect(register)
        elif User.objects.filter(username=email).exists():
            messages.info(request,'email is already taken ')
            return redirect(register)
        elif password!=confirm_password:
            messages.error(request,'password do not match')
            return redirect(register)
        else:

            otp = get_random_string(length=6,allowed_chars='1234567890')

            user=User.objects.create_user(username=email,password=password,first_name=username)

            subject='otp for account varification'
            message=f'your otp for account varification is {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list =[email,]
            send_mail(subject,message,email_from,recipient_list)

            UserProfile.objects.create(user=user)

            user.profile.otp = otp
            user.profile.save()
            return redirect('verify_otp',user.id)

    return render(request,'user/register.html')

def verify_otp(request,user_id):
    user=User.objects.get(id=user_id)
    if request.method =='POST':
        otp = request.POST['otp']
        if user.profile.otp == otp:
            user.profile.is_verified=True
            user.profile.otp=''
            user.profile.save()
            messages.success(request,'account has been verified')
            return redirect(loginpage)
        else:
            messages.error(request,'invalid otp')
            return redirect('verify_otp',user_id)
    return render(request,'user/verifyotp.html',{'user':user})    

def resend_otp(request, user_id):
    user = User.objects.get(id=user_id)

    # Generate new OTP
    otp = get_random_string(length=6, allowed_chars='1234567890')

    # Send new OTP to user email
    subject = 'New OTP for account verification'
    message = f'Your new OTP for account verification is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.username,]
    send_mail(subject, message, email_from, recipient_list)

    # Save new OTP to database
    user.profile.otp = otp
    user.profile.save()

    messages.success(request, 'New OTP has been sent to your email')
    return redirect('verify_otp', user_id)


def forgotpassword(request):
    if request.method =='POST':
        email=request.POST['email']
        if User.objects.filter(username=email).exists():
            user=User.objects.get(username=email)
            otp = get_random_string(length=6,allowed_chars='1234567890')
            user.profile.otp=otp
            user.profile.save()
            subject='otp for password reset'
            message=f'your OTP for reset password is{otp}'
            email_form=settings.EMAIL_HOST_USER
            recipient_list=[email,]
            send_mail(subject,message,email_form,recipient_list)
            return redirect('resetpassword',user.id)
        else:
            message.error(request,'Email does not exist')
            return redirect(forgotpassword)

    return render(request,'user/forgotpassword.html')

def resetpassword(request,user_id):
    user=User.objects.get(id=user_id)
    if request.method== 'POST':
        otp = request.POST['otp']
        if user.profile.otp == otp:
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password == confirm_password:
                user.set_password(password)
                user.profile.otp =''
                user.profile.save()
                user.save()
                messages.success(request,'password reset successfull please login')
                return redirect('loginpage')
            else:
                messages.error(request,'password do not match')
        else: 
            messages.error(request,'invalid otp')
    return render(request,'user/resetpassword.html',{'user':user})      

def userprofile(request)    :
    return render(request,'user/userprofile.html')   

def address_book(request):
    addresses = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        selected_addresses = request.POST.getlist('selected_addresses')
        Address.objects.filter(id__in=selected_addresses).delete()
        return redirect(address_book)
    return render(request, 'user/address_book.html', {'addresses': addresses})


def add_address(request,id):
    state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
    city = ['Kannur','Kozhikkode','Ernakulam','Thiruvananthapuram','Banglore','Hubli','Hydrabad','Coimbator','Madurai']
    addresse=Address.objects.all()
    
    if request.method == 'POST':
        address = Address(
            user=request.user,
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            address_line_1=request.POST['address_line_1'],
            address_line_2=request.POST.get('address_line_2', ''),
            # phone=request.POST['phone'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode']
        )
        if addresse.count() >= 3:
            messages.warning(request, 'You have reached the maximum limit of 5 addresses.')
        else:
            address.save()
        if id == 1:
            return redirect('checkout')
        else:
            return redirect(address_book)
        
        
    context = {
        'state': state,
        'city': city,
    }
    return render(request,'user/add_address.html',context)

def updateprofile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=user_profile)
    if request.user.is_superuser:
        return redirect('userprofile')

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save()
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            user_profile = profile.save()
            messages.info(request, 'Updated Successfully')
            return redirect('userprofile')

    if request.user.is_superuser and request.user == user_profile.user:
        messages.error(request, 'Superusers cannot update their own profiles')
        return redirect('userprofile')

    return render(request, 'user/updateuserprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def changepassword(request):
    if request.method == 'POST':
        oldpass = request.POST['currentpassword']
        newpass = request.POST['newpassword']
        confirm_newpass = request.POST['confirmpassword']
        user = authenticate(username=request.user.username, password=oldpass)
        if user:
            if newpass == confirm_newpass:
                user.set_password(newpass)
                user.save()
                messages.success(request, "Password Changed")
                return redirect(loginpage)
            else:
                messages.success(request, "Password not matching")
                return redirect(changepassword)
        else:
            messages.success(request, "Invalid Password")
            return redirect(changepassword)
        
    return render(request, 'user/changepassword.html')

def edit_address(request, address_id):
    state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
    city = ['Kannur','Kozhikkode','Ernakulam','Thiruvananthapuram','Banglore','Hubli','Hydrabad','Coimbator','Madurai']
    newaddress = Address.objects.get(id= address_id)
    
    if request.method == 'POST':
        newaddress.firstname=request.POST['firstname']
        newaddress.lastname=request.POST['lastname']
        newaddress.email=request.POST['email']
        newaddress.address_line_1=request.POST['address_line_1']
        newaddress.address_line_2=request.POST.get('address_line_2', '')
        newaddress.phone=request.POST['phone']
        newaddress.city=request.POST['city']
        newaddress.state=request.POST['state']
        newaddress.pincode=request.POST['pincode']
        newaddress.save()
        return redirect(address_book)
    
    context = {
        'state': state,
        'city' : city,
        'newaddress' : newaddress
    }

    return render(request, 'user/edit_address.html',context)

# def userproduct(request, id):
#     if id == 0:
#         product = Product.objects.all()
        
#     else:
#         category = Category.objects.get(id=id)
#         product = Product.objects.filter(category=category)
        
#     paginator = Paginator(product, 6)
#     page_numebr = request.GET.get('page')
#     page_obj = paginator.get_page(page_numebr)
#     varient=ProductVarient.objects.all()
#     allcategory = Category.objects.all() 
#     context = {
#         'product':product,
#         'allcategory':allcategory,
#         'page_obj':page_obj,
#         'varient':varient
#     }       
#     return render(request, 'user/userproduct.html', context)


def userproduct(request, id):
    if id == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=id)
        product = Product.objects.filter(category=category)

    paginator = Paginator(product, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    allcategory = Category.objects.all()
    context = {
        'product': product,
        'allcategory': allcategory,
        'page_obj': page_obj
    }
    return render(request, 'user/userproduct.html', context)

# def review(request):
#     prod = Product.objects.get(id=id)

#     if request.method == 'POST':
#         if 'username' in request.session:
#             feedback = request.POST.get('message')
#             user=request.user
#             reviews= Review(user=user,feedback=feedback)
#             reviews.save()
#             reviews.product.set([prod])
#             messages.info(request,'thank you for your valuable feedback ')  # Use set() to add the product to the relationship
#             return redirect('usersingleproduct',id=id)
#         messages.info(request,"please login and your review") 

def usersingleproduct(request, id):
    

    prod = Product.objects.get(id=id)
    images = ProductImage.objects.filter(product_id=id)
    variant = ProductVarient.objects.filter(proname=prod)
    variant_price = ProductVarient.objects.filter(proname=prod).first()
    

    reviews = Review.objects.filter(products=prod)

    if request.method == 'POST':
        
        selected_value=request.POST.get('selected_value')
        if selected_value is None:
            messages.warning(request, 'Please select a variant')
            return redirect('usersingleproduct', id=id)
        
        selected_variant = ProductVarient.objects.get(proname=prod,varientname=selected_value)
        print(selected_variant,'-----------varirnt----------')
        print(selected_variant.id)
        
        
        # messages.info(request,'thank you for your valuable feedback ')  # Use set() to add the product to the relationship
        n= render_to_string('user/price.html',{"selected_variant":selected_variant})
        return JsonResponse({'data':n})

    return render(request, 'user/usersingleproduct.html', locals())


def search(request):
    keyword = request.GET.get('keyword')
    products = Product.objects.filter(Q(description__icontains=keyword) | Q(name__icontains=keyword)).order_by('created')
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    allcategory = Category.objects.all() 
    context = {
        'categories': Category.objects.all(),
        'product': products,
        'keyword' : keyword,
        'allcategory' : allcategory,
        'page_obj': page_obj
        
        
    }
    return render(request, 'user/userproduct.html', context)

def viewOrder(request, id):
    order =Order.objects.filter(id=id,user=request.user).first()
    orderitems = OrderProduct.objects.filter(order=order)
    
    context={
        'order': order,
        'orderitems':orderitems,
    }
    return render(request,'user/vieworder.html',context)
 



def myorders(request):
    orders=Order.objects.filter(user=request.user).order_by('created_at')
    context ={
        'orders':orders
    }

    return render(request,'user/myorders.html',context)

def cancelOrder(request,id):

#    client = razorpay.Client(auth=("rzp_test_P2idDWJHzXlYX7", "4RlxwFkFp4gvf8sMSzhOfxlt"))

   client = razorpay.Client(auth=(e_commerce.settings.API_KEY, e_commerce.settings.RAZORPAY_SECRET_KEY))
   order = Order.objects.get(id=id,user=request.user)
   payment=order.payment
   msg=''
   if (payment.payment_method == 'Paid by Razorpay'):
      payment_id = payment.payment_id
      amount = payment.amount_paid
      amount=amount*100
      print(amount)
      print('ttttttttttttttttttttttttttttttttttt')
      captured_amount = client.payment.capture(payment_id,amount)
      print(captured_amount)

      if captured_amount['status'] == 'captured' :
         refund_data = {
            "payment_id": payment_id,
            "amount": amount,  # amount to be refunded in paise
            "currency": "INR",
         }
      else:
         msg = "Your bank has not completed the payment yet."
         # If the payment is not captured, return an error message and don't attempt a refund
         orderitems = OrderProduct.objects.filter(order=order)
         context={
            'order': order,
            'orderitems':orderitems,
            'msg':msg
         }
         return render(request,'user/vieworder.html',context)
      refund = client.payment.refund(payment_id, refund_data)
      print(refund)
      if refund is not None:
         current_user=request.user
         order.refund_completed = True
         order.status = 'Cancelled'
         payment = order.payment
         payment.refund_id = refund['id']
         payment.save()
         order.save()
         msg ="Your order has been successfully cancelled and amount has been refunded!"
         mess=f'Hello\t{current_user.first_name},\nYour order has been canceled,Money will be refunded with in 1 hour\nThanks!'
         send_mail(
                        "Hoely Furnitures - Order Cancelled",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [current_user.email],
                        fail_silently = False
                     )
      else :
         msg ="Your order is not cancelled because the refund couldnot be  completed now. Please try again later. If the issue continues, CONTACT THE SUPPORT TEAM!"
         pass
   else :
      if(payment.paid):
         order.refund_completed = True
         order.status = 'Cancelled'
         msg ="YOUR ORDER HAS BEEN SUCCESSFULLY CANCELLED!"
         order.save()
      else:
         order.status = 'Cancelled'
         order.save()
         msg ="Your payment has not been recieved yet. But the order has been cancelled.!"
   orderitems = OrderProduct.objects.filter(order=order)
   context={
        'order': order,
        'orderitems':orderitems,
        'msg':msg
    }
   return render(request,'user/vieworder.html',context)

def logout(request):  #LOGOUT REQUEST
      auth.logout(request)
      return redirect(base)



