from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User,auth
from .models import Category,Product,ProductImage,ProductVarient,Banner
from django.core.paginator import Paginator
from productapp.models import Coupon,Order,Payment
from django.shortcuts import get_object_or_404
from .forms import CouponForm
from django.db.models import Sum




# Create your views here.




def adminlogin(request):
    
    if request.user.is_superuser:
        return redirect('bases')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('bases')  # Replace 'superuser_dashboard' with your superuser dashboard URL name
        else:
            messages.info(request,'Invalid Username or Password')
    return render(request, 'admin/adminlogin.html')



def addcategory(request):
    if request.method == "POST":
        name = request.POST['name']
        if Category.objects.filter(name__iexact=name.lower().replace(' ', '')).exists():
            messages.error(request,'category already exist')

        else:
            Category.objects.create(name=name)
            messages.success(request,'category created successfully')
            return redirect(viewcategory)
    return render(request, 'admin/addcategory.html', locals())

def viewcategory(request):
    category = Category.objects.all()
    return render(request, 'admin/viewcategory.html', locals()) 

def editcategory(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == 'POST':
        name = request.POST['name']
        if Category.objects.filter(name__iexact=name.lower().replace(' ', '')).exists():
            messages.info(request,"Category already exists")  
        else:
            category.name = name
            category.save()
            messages.success(request,'category edited successfully')
            return redirect(viewcategory)
        
    return render(request, 'admin/editcategory.html', locals())

def deletecategory(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request,'category deleted successfully')
    return redirect(viewcategory)

def addproduct(request):
    category = Category.objects.all()
    if request.method == 'POST':
        name = request.POST['name']

        categ = request.POST['categories']
        desc = request.POST['desc']
        images = request.FILES.getlist('image')
        catobj = Category.objects.get(id=categ)
        product = Product.objects.create(name=name,category=catobj, description=desc)
        product.save()
        for image in images:
            ProductImage.objects.create(product=product, images=image)
        messages.success(request, "Product Added")
        return redirect(viewproduct)
    return render(request, 'admin/addproduct.html',locals())

def viewproduct(request):
    product = Product.objects.all().order_by('id')
    varient= ProductVarient.objects.all()
    paginator = Paginator(product, 6)
    page_numebr = request.GET.get('page')
    page_obj = paginator.get_page(page_numebr)
    
    dict_prod = {
        'product' : product,
        'page_obj': page_obj,
        'varient':varient
    }
    return render(request, 'admin/viewproduct.html',dict_prod)

def editproduct(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    images = ProductImage.objects.filter(product=product)
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        desc = request.POST['desc']
        catobj = Category.objects.get(id=cat)
        
        if int(price) < 0:
            messages.warning(request,"Enter a valid quantity")
            return redirect(editproduct,pid)
        else:

        # Update product attributes
            Product.objects.filter(id=pid).update(name=name, price=price, category=catobj, description=desc)

        # Get the new images uploaded during editing
        new_images = request.FILES.getlist('images')

        # Add the new images to the product
        for image in new_images:
            ProductImage.objects.create(product=product, images=image)
       
        messages.success(request, "Product Updated")
        return redirect(viewproduct)
    return render(request, 'admin/editproduct.html', locals())

def deleteproduct(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect(viewproduct)


def addvarient(request):
    products = Product.objects.all()
    if request.method == 'POST':
        product_id = request.POST['product']
        prod_varientname = request.POST['varname']
        stock = request.POST['stock']
        varientprice=request.POST['price']

        product = Product.objects.get(id=product_id)
        if int(stock) < 0 :
            messages.warning(request,'Enter a valid Quantity')
        else:
            # if ProductVarient.objects.filter(varientname__iexact=prod_varientname.lower().replace(' ', '')).exists(): 
            #     messages.warning(request,'The varient name with the same product already exists')
            # else:
                productvarient = ProductVarient.objects.create(varientname=prod_varientname,varprice=varientprice,varstock=stock,proname=product)
                productvarient.save()
                messages.success(request, 'varient added successfully')
                return redirect(viewvarient)
    context = {
       'products': products,
    }
    return render(request, 'admin/add_varient.html', context)


def viewvarient(request):
    varient = ProductVarient.objects.all().order_by('id')
    context = {
        'varient':varient,
    }

    return render(request, 'admin/view_varient.html',context)

def editvarient(request,id):
    product = Product.objects.all()
    provarient = ProductVarient.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST['products']
        varname = request.POST['varname']
        stock = request.POST['stock']
        if int(stock) < 0:
            messages.warning(request,"Enter a valid quantity")
        else:
            ProductVarient.objects.filter(id=id).update(varientname=varname,varstock=stock,proname=name)
            messages.success(request, ' varient edited successfully')
            return redirect(viewvarient)
    context = {
        'product':product,
        'provarient':provarient,
    }
    return render(request,'admin/edit_varient.html',context)


def deleteverient(request,id):
    productvar = ProductVarient.objects.get(id=id)
    productvar.delete()
    messages.success(request, "Product Deleted")
    return redirect(viewvarient)





@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def bases(request):
    # Your superuser dashboard code goes here
    return render(request,'admin/bases.html')

def adminlogout(request):
    auth.logout(request)
    if 'username' in request.session:
        request.session.flush()
    return redirect(adminlogin)    


def view_coupons(request):
    coupons = Coupon.objects.all()
    return render(request,'admin/view_coupons.html',{'coupons':coupons})

def add_coupons(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_coupons')
    else:
        form = CouponForm()
    return render(request, 'admin/add_coupons.html', {'form': form})

def edit_coupon(request, pid):
    coupon = Coupon.objects.get(id=pid)

    if request.method == "POST":
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon Updated")
            return redirect('view_coupons')
    else:
        form = CouponForm(instance=coupon)
        messages.error(request, "fill all fields")

    return render(request, 'admin/edit_coupon.html', {'form': form, 'coupon': coupon})


def delete_coupon(request, pid):
    coupon = Coupon.objects.get(id=pid)
    coupon.delete()
    messages.success(request, "Coupon Deleted")
    return redirect('view_coupons')


def manageuser(request):
    user = User.objects.all().order_by('id')[1:]

    return render(request, 'admin/manage_user.html', {'user': user})

def blockuser(request, id):
    user = get_object_or_404(User, id=id)
    if user.is_active:
        user.is_active = False
        messages.success(request, "user has been blocked.")
    else:
        user.is_active = True
        messages.success(request, "user has been unblocked.")
    user.save()
    return redirect(manageuser)


def manage_order(request):
    orders=Order.objects.all().order_by('id')
    paginator = Paginator(orders, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render(request, 'admin/manageorder.html', locals())

def update_order(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        status = request.POST.get('status')
        if(status):
            order.status = status
            order.save()
        if status  == "Delivered":
            try:
                payment = Payment.objects.get(payment_id = order.order_number, status = False)
                print(payment)
                if payment.payment_method == 'Cash on Delivery':
                    payment.paid = True
                    payment.save()
            except:
                pass
    return redirect('manage_order')

def admindashboard(request):
    user=User.objects.all().count()
    product=Product.objects.all().count()
    category=Category.objects.all().count()
    order=Order.objects.all().count()
    coupons=Coupon.objects.all().count()
    total_income = Payment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum']
            
    context={
        'user':user,
        'product':product,
        'category':category,
        'order':order,
        'coupons':coupons,
        'total_income' :total_income,

    }
    return render(request,'admin/admindashboard.html',context)

def addbanner(request):
    if request.method == 'POST':
        title=request.POST['title']
        image=request.FILES['image']
        discription=request.POST['discription']
        banner=Banner.objects.create(title=title,image=image,discription=discription)
        banner.save()
        messages.info(request,'banner added succesfully')
        return redirect(viewbanner)



    return render(request,'admin/addbanner.html')

def viewbanner(request):
    banner=Banner.objects.all()
    return render(request,'admin/viewbanner.html',locals())

def editbanner(request, pid):
    banner = Banner.objects.get(id=pid)
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['discription']
        new_image = request.FILES.get('image')
        if new_image:
            # delete the old image
            if banner.image:
                banner.image.delete()
            # save the new image to the same path
            banner.image = new_image
        banner.title = title
        banner.desc = desc
        banner.save()

        messages.success(request, 'Banner edited successfully')
        return redirect('viewbanner')
    
    context = {'banner': banner}
    return render(request, 'admin/editbanner.html', context)

def deletebanner(request,pid):
    banner=Banner.objects.get(id=pid)
    banner.delete()
    messages.success(request,'banner deleted successfully')
    return redirect(viewbanner)

