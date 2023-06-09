
from django.shortcuts import render ,redirect
from .models import wishlist ,CartItem,Coupon,UserCoupon,Order,Payment,OrderProduct
from adminapp.models import Product,ProductVarient
from django.contrib import messages
from django.contrib.auth.models import User
from userapp.views import loginpage
from userapp.models import Address
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import datetime
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import e_commerce.settings
# import razorpay

# Create your views here.

def userwishlist(request):
    user = request.user
    witems=wishlist.objects.filter(user_id=user.id)
    

    return render(request,'product/wishlist.html',{'witems':witems})



@login_required(login_url='loginpage')
def add_to_wishlist(request, product_id):
    # product = Product.objects.get(id=product_id)
    varient = ProductVarient.objects.get(id=product_id)
    product = varient.proname
    user = request.user
    
    if wishlist.objects.filter(product=product, user_id=user.id,provar=varient).exists():
        messages.info(request, "Product already exists in wishlist.")
    else:
        wishlist.objects.create(product=product, user_id=user.id,provar=varient)
        messages.success(request, "Product added to wishlist.")
    return redirect('userwishlist')
    
def remove_from_wishlist(request,product_id,varient_id):
    user = request.user
    wishItem=wishlist.objects.get(product_id=product_id,user_id=user.id,provar_id=varient_id)
    wishItem.delete()
    return redirect(userwishlist)


def viewcart(request):
    current_user = request.user
    items = CartItem.objects.filter(user_id=current_user.id).order_by('id')
    cart_items = []
    total = 0
    for cart_item in items:
        try:
            product = Product.objects.get(id=cart_item.product_id)
        except Product.DoesNotExist:
            # Handle the case where the product does not exist
            messages.info(request,"there is no product in view cart")   
            return redirect(viewcart)

        varient=ProductVarient.objects.get(id=cart_item.provar.id)
        quantity = cart_item.quantity
        price = cart_item.provar.varprice*quantity
        
        cart_items.append({'product':product,'varient':varient,'quantity':quantity,'price':price}) 
        if varient.varstock == 0:
            messages.info(request,"there is no stock for this product")
            return redirect('userproduct',0)
        else:
            total += price   
    context = { 'cart_items': cart_items, 'total': total }

    return render(request, 'product/viewcart.html',context)


@login_required(login_url='loginpage')
def addtocart(request, product_id):
    current_user=request.user
    quantity = request.POST.get('quantity')
    if quantity is None:
        product_quantity = 1
    else:
        product_quantity= int(quantity)

    # try:
    #     product = Product.objects.get(id=product_id)
    # except ObjectDoesNotExist:
    #     messages.error(request,"there is no product")
    #     return redirect('userproduct',0)
    if request.method == 'POST':
        varient_id=request.POST.get('varient_id')
        print(varient_id,'------------in if-------')
    else:
        varient =ProductVarient.objects.get(id=product_id)
        varient_id = varient.varientname
        print(varient_id,'------------in else-------')
    
    try:
        varient=ProductVarient.objects.get(varientname=varient_id)
        product= varient.proname
        print(product,'-------product in add to cart----')
    except ObjectDoesNotExist :
        messages.info(request,"please select the varient")
        return redirect('usersingleproduct',product_id)   

    item_exists = CartItem.objects.filter(user_id=current_user.id,product_id=product.id ,provar_id=varient.id).exists()
    if (item_exists):
        item=CartItem.objects.get(product_id=product.id,user_id=current_user.id,provar_id=varient.id)
        quantity_expected=item.quantity + product_quantity
        if varient.varstock>quantity_expected:

            item.quantity = item.quantity + product_quantity
            item.save()
            messages.success(request,  f"{product.name} are added to Cart.")
        else:

            item.quantity = varient.varstock
            item.save()
            messages.info(request,  f"{varient.varstock} items left. All of them are added to Cart.")
    else:
        if(varient.varstock>=product_quantity):
            item = CartItem.objects.create(user_id=current_user.id, product_id=product.id,quantity=product_quantity,provar_id=varient.id)
            messages.success(request, f"{product.name} added to cart!")
        else:
            product_quantity = varient.varstock
            item = CartItem.objects.create(user_id=current_user.id, product_id=product.id,quantity=product_quantity,provar_id=varient.id)
            messages.info(request,  f"{varient.varstock} items left. All of them are added to Cart.")

    return redirect(viewcart)
    



def removecartproduct(request,product_id,varient_id):
    current_user = request.user
    try:
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        messages.error(redirect,"no more product")
        
    varient=ProductVarient.objects.get(id=varient_id)
    cart_item=CartItem.objects.get(user_id=current_user.id,product_id=product.id,provar=varient)
    cart_item.delete()
    return redirect(viewcart)


@login_required
def addcartitem(request,product_id,varient_id):
    current_user=request.user
    try:
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        messages.error(request,"there is no more stock left")
        return redirect(viewcart)

    varient=ProductVarient.objects.get(id=varient_id)
    item=CartItem.objects.get(user_id=current_user.id, product=product,provar=varient)
    item.quantity = item.quantity + 1
    if (varient.varstock>item.quantity):
        item.save()
        return redirect(viewcart)
    else:
        messages.warning(request,"Product Out Of Stock...! Can't be added to cart")
        return redirect(viewcart)

    
    
def removecartitem(request,product_id,varient_id):
    current_user = request.user
    try:
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        return redirect(viewcart)
    varient=ProductVarient.objects.get(id=varient_id)

    cart_items = CartItem.objects.filter(user_id=current_user.id, product=product,provar=varient)
     
    for cart_item in cart_items:
        if cart_item.quantity == 1:
            cart_item.delete()  # remove the item from the cart if the quantity is 1
        else:
            cart_item.quantity -= 1
            cart_item.save()  # decrement the quantity by 1
    return redirect(viewcart)    



# def checkout(request):
#     state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
#     city = ['Kannur','Kozhikkode','Ernakulam','Thiruvananthapuram','Banglore','Hubli','Hydrabad','Coimbator','Madurai']
#     couponcodes=Coupon.objects.all()
#     subtotal=0
#     quantity=0
#     amountToBePaid =0
#     msg=''
#     cart_items=None
#     coupon_discount = 0
#     coupon_code = ''
#     discount = False
#     coupon = ''
    
#     addresses = Address.objects.filter(user_id=request.user)
#     # selected_address = addresses.first() if selected_address else None
#     user=User.objects.get(id=request.user.id)
#     cart_items=CartItem.objects.filter(user=user, provar__varstock__gt=0)
#     for cart_item in cart_items:
#         subtotal+=(cart_item.provar.varprice*cart_item.quantity)
#         quantity+=cart_item.quantity
#     grand_total = subtotal+70
#     amountToBePaid = grand_total
#     if ('couponCode' in request.POST):
#         coupon_code = request.POST.get('couponCode')
#         print('checkout il cuopon')
#         print(coupon_code)
#         try:
#             coupon = Coupon.objects.get(code = coupon_code)
#             couponcodes=Coupon.objects.all()
#             grand_total = request.POST['grand_total']
#             coupon_discount = 0
#             if (coupon.active):
#                 try:
#                     instance = UserCoupon.objects.get(user=request.user, coupon=coupon)
#                 except ObjectDoesNotExist:
#                     instance = None
#                 # instance = UserCoupon.objects.get(user = request.user ,coupon = coupon)
#                 if(instance):
#                     pass
#                 else:
#                     instance = UserCoupon.objects.create(user = request.user ,coupon = coupon)
#                 if(not instance.used):
#                     if float(grand_total) >= float(instance.coupon.min_value):
#                         coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
#                         amountToBePaid = float(grand_total) - coupon_discount
#                         amountToBePaid = format(amountToBePaid, '.2f')
#                         coupon_discount = format(coupon_discount, '.2f')
#                         msg = 'Coupon Applied successfully'
#                         discount=True
#                     else:
#                         msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
#                 else:
#                     msg = 'Coupon is already used'
#             else:
#                 msg="Coupon is not Active!"
#         except:
#             msg="Invalid Coupon Code!"
#     else:
#         try:
#             instance = UserCoupon.objects.get(user=request.user, used= False)
#             instance.delete()
#         except ObjectDoesNotExist:
#             instance = None
#     rkey=e_commerce.settings.API_KEY
#     context={
#         'subtotal':subtotal,
#         'quantity':quantity,
#         'cart_items':cart_items,
#         'grand_total':grand_total,
#         'user':user,
#         'amountToBePaid':amountToBePaid,
#         'msg':msg,
#         'coupon':coupon,
#         'coupon_discount':coupon_discount,
#         'discount':discount,
#         'AllAddress':addresses,
#         'state':state,
#         'city':city,
#         'couponcodes':couponcodes,
#         'rkey':rkey
#         #'selected_address':selected_address
#     }
#     return render(request,'product/checkout.html',context)

@login_required
def checkout(request):
    state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
    city = ['Kannur', 'Kozhikkode', 'Ernakulam', 'Thiruvananthapuram', 'Banglore', 'Hubli', 'Hydrabad', 'Coimbator', 'Madurai']
    couponcodes = Coupon.objects.all()
    subtotal = 0
    quantity = 0
    amountToBePaid = 0
    msg = ''
    cart_items = None
    coupon_discount = 0
    coupon_code = ''
    discount = False
    coupon = ''
    
    addresses = Address.objects.filter(user_id=request.user)
    if not addresses: 
        messages.error(request,'You have not added any addresses. Please add an address to continue.')
        return redirect('useraddress')
    else:

        user = User.objects.get(id=request.user.id)
        cart_items = CartItem.objects.filter(user=user, provar__varstock__gt=0)

        for cart_item in cart_items:
            subtotal += (cart_item.provar.varprice*cart_item.quantity)
            quantity += cart_item.quantity

        grand_total = subtotal+70
        amountToBePaid = grand_total

        if ('couponCode' in request.POST):
            coupon_code = request.POST.get('couponCode')
            print('checkout il cuopon')
            print(coupon_code)
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                couponcodes = Coupon.objects.all()
                grand_total = request.POST['grand_total']
                coupon_discount = 0

                if (coupon.active):
                    try:
                        instance = UserCoupon.objects.get(user=request.user, coupon=coupon)
                    except ObjectDoesNotExist:
                        instance = None

                    if(instance):
                        pass
                    else:
                        instance = UserCoupon.objects.create(user=request.user, coupon=coupon)

                    if(not instance.used):
                        if float(grand_total) >= float(instance.coupon.min_value):
                            coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
                            amountToBePaid = float(grand_total) - coupon_discount
                            amountToBePaid = format(amountToBePaid, '.2f')
                            coupon_discount = format(coupon_discount, '.2f')
                            msg = 'Coupon Applied successfully'
                            discount = True
                        else:
                            messages.info(request,'This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!')
                    else:
                        messages.info(request,'Coupon is already used')
                else:
                    messages.info(request,"Coupon is not Active!")
            except:
                messages.error(request,"Invalid Coupon Code!")
        else:
            try:
                instance = UserCoupon.objects.get(user=request.user, used=False)
                instance.delete()
            except ObjectDoesNotExist:
                instance = None

        context = {
            'subtotal': subtotal,
            'quantity': quantity,
            'cart_items': cart_items,
            'grand_total': grand_total,
            'user': user,
            'amountToBePaid': amountToBePaid,
            'msg': msg,
            'coupon': coupon,
            'coupon_discount': coupon_discount,
            'discount': discount,
            'AllAddress': addresses,
            'state': state,
            'city': city,
            'couponcodes': couponcodes,
            'rkey': e_commerce.settings.API_KEY
        }
        return render(request,'product/checkout.html',context)


def calculateCartTotal(request):
   cart_items   = CartItem.objects.filter(user=request.user,provar__varstock__gt=0)
   if not cart_items:
       pass
    #   return redirect('product_management:productlist',0)
   else:
      total = 0
      tax=0
      grand_total=0
      for cart_item in cart_items:
         total  += (cart_item.provar.varprice * cart_item.quantity)
         tax =70
         grand_total = tax + total
   return total, tax, grand_total



def placeOrder(request):
   if request.method =='POST':
         if ('couponCode' in request.POST):
            instance = checkCoupon(request)
         cart_items  = CartItem.objects.filter(user=request.user,provar__varstock__gt=0)
         if not cart_items:
            return redirect('userproduct',0)
         newAddress_id = request.POST.get('selected_addresses')
         print(newAddress_id)
         address  = Address.objects.get(id = newAddress_id)
         newOrder =Order()
         newOrder.user=request.user
         newOrder.address = address
         yr = int(datetime.date.today().strftime('%Y'))
         dt = int(datetime.date.today().strftime('%d'))
         mt = int(datetime.date.today().strftime('%m'))
         d = datetime.date(yr,mt,dt)
         current_date = d.strftime("%Y%m%d")
         rand = str(random.randint(1111111,9999999))
         order_number = current_date + rand
         newPayment = Payment()
         if('payment_id' in request.POST ):
            newPayment.payment_id = request.POST.get('payment_id')
            newPayment.paid = True
         else:
            newPayment.payment_id = order_number
            payment_id  =order_number
         newPayment.payment_method = request.POST.get('payment_method')
         newPayment.customer = request.user
         newPayment.save()
         newOrder.payment = newPayment
         total, tax, grand_total = calculateCartTotal(request)
         newOrder.order_total = grand_total
         if(instance):
            if(instance.used == False):
                if float(grand_total) >= float(instance.coupon.min_value):
                    coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
                    amountToBePaid = float(grand_total) - coupon_discount
                    amountToBePaid = format(amountToBePaid, '.2f')
                    coupon_discount = format(coupon_discount, '.2f')
                    print(coupon_discount,'----------------------------------------')
                    newOrder.order_discount = coupon_discount
                    newOrder.paid_amount = amountToBePaid
                    instance.used = True
                    newOrder.paid_amount = amountToBePaid
                    newPayment.amount_paid = amountToBePaid
                    instance.save()
                else:
                    msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
            else:
                newOrder.paid_amount = grand_total
                newPayment.amount_paid = grand_total
                newOrder.discount=0
                msg = 'Coupon is not valid'
         else:
            newOrder.paid_amount = grand_total
            newPayment.amount_paid = grand_total
            msg = 'Coupon not Added'
         newPayment.save()
         newOrder.payment = newPayment
         order_number = 'Trinity'+ order_number
         newOrder.order_number =order_number
         #to making order number unique
         while Order.objects.filter(order_number=order_number) is None:
            order_number = 'Trinity'+order_number
         newOrder.tax=tax
         newOrder.save()
         newPayment.order_id = newOrder.id
         newPayment.save()
         newOrderItems = CartItem.objects.filter(user=request.user)
         

         for item in newOrderItems:
            OrderProduct.objects.create(
                order = newOrder,
                customer=request.user,
                productvarient=item.provar,
                product=item.product,
                product_price=item.provar.varprice,
                quantity=item.quantity
            )
            product_varient = item.provar
            product_varient.varstock -= item.quantity
            product_varient.save()
            # #TO DECRESE THE QUANTITY OF PRODUCT FROM CART
            # orderproduct = Product.objects.filter(id=item.product_id).first()
            # if(orderproduct.stock<=0):
            #    messages.warning(request,'Sorry, Product out of stock!')
            #    orderproduct.is_available = False
            #    orderproduct.save()
            #    item.delete()
            #    return redirect('order_management:cart')
            # elif(orderproduct.stock < item.quantity):
            #    messages.success(request,  f"{orderproduct.stock} only left in cart.")
            #    return redirect('order_management:cart')
            # else:
            #    orderproduct.stock -=  item.quantity
            # orderproduct.save()
         if(instance):
            instance.order = newOrder
            instance.save()
        # TO CLEAR THE USER'S CART
         cart_item=CartItem.objects.filter(user=request.user,provar__varstock__gt=0)
         cart_item.delete()
         messages.success(request,'Order Placed Successfully')
         payMode =  request.POST.get('payment_method')
         if (payMode == "Paid by Razorpay" ):
            return JsonResponse ({'status':"Your order has been placed successfully"})
         elif (payMode == "COD" ):
            request.session['my_context'] = {'payment_id':payment_id}
            return redirect('order_complete')
   return redirect('checkout')


def checkCoupon(request):
   try:
      coupon_code = request.POST['couponCode']
      print('coupon in checkcoupon')
      print(coupon_code)
      coupon = Coupon.objects.get(code = coupon_code)
      try:
         instance = UserCoupon.objects.get(user=request.user, coupon=coupon)
      except ObjectDoesNotExist:
         instance = None
         if(instance):
            pass
         else:
            instance = UserCoupon.objects.create(user = request.user ,coupon = coupon)
   except:
      instance = None
   return instance




def razorPayCheck(request):
    total=0
    coupon_discount =0
    amountToBePaid = 0
    current_user=request.user
    cart_items=CartItem.objects.filter(user_id=current_user.id,provar__varstock__gt=0)
    print(cart_items)
    if cart_items:
        for cart_item in cart_items:
            total+=(cart_item.provar.varprice*cart_item.quantity)
        tax=(5 * total)/100
        grand_total=total+tax
        grand_total = round(grand_total,2)
        try:
            instance = UserCoupon.objects.get(user=request.user, used=False)
            coupon = instance.coupon.code
            if float(grand_total) >= float(instance.coupon.min_value):
                coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
                amountToBePaid = float(grand_total) - coupon_discount
                amountToBePaid = format(amountToBePaid, '.2f')
                coupon_discount = format(coupon_discount, '.2f')
        except ObjectDoesNotExist:
            instance = None
            amountToBePaid = grand_total
            coupon_discount = 0
            coupon =None
        return JsonResponse({
            'grand_total' : grand_total,
            'coupon': coupon,
            'coupon_discount':coupon_discount,
            'amountToBePaid':amountToBePaid
        })
    else:
        return redirect('userproduct',0)
   

def orderComplete(request):
    product_items = []
    total=0
    if ('payment_id' in request.GET):
      payment_id = request.GET.get('payment_id')
      print(payment_id,'22222222')
      payment = Payment.objects.get(payment_id=payment_id)

    else:
      try:
         my_context = request.session.get('my_context', {})
         payment_id = my_context['payment_id']
         print(payment_id,'11111111')
         payment = Payment.objects.get(payment_id=payment_id)
      except:
         user=request.user
         payment = Payment.objects.filter(customer=user, payment_method ='COD').order_by('-created_at').first()

    order_details = Order.objects.get(payment=payment)
    print(order_details,'33333333')
    orderitems = OrderProduct.objects.filter(order=order_details.id)
    for order_item in orderitems:
            product = Product.objects.get(id=order_item.product.id)
                 
            quantity = order_item.quantity
            price = order_item.productvarient.varprice * quantity
            total += price
            product_items.append({
                'product': product,
                'quantity': quantity,
                'price': price
            })
    context={
        'total':total,
        'order': order_details,
        'orderitems':orderitems,
        'product_items': product_items,
    }

    return render(request,'product/order_complete.html',context)

