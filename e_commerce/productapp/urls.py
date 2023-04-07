from . import views
from django.urls import path

urlpatterns = [

    path('wishlist/',views.userwishlist,name='userwishlist'),
    path('addwishlist/<int:product_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('removewishlist/<int:product_id>/<int:varient_id>/',views.remove_from_wishlist,name='remove_from_wishlist'),

    path('viewcart', views.viewcart, name="viewcart"),
    path('addtocart/<int:product_id>/', views.addtocart, name='addtocart'),
    path('removecartproduct/<int:product_id>/<int:varient_id>/',views.removecartproduct,name='removecartproduct'),
    path('addcartitem/<int:product_id>/<int:varient_id>/',views.addcartitem,name='addcartitem'),
    path('removecartitem/<int:product_id>/<int:varient_id>/',views.removecartitem,name='removecartitem'),
   
    path('checkout/',views.checkout,name='checkout'),
    path('proceed_to_pay/',views.razorPayCheck,name="razorpaycheck"),
    path('place_order/', views.placeOrder, name='place_order'),
    path('ordercomplete/',views.orderComplete, name='order_complete'),



]