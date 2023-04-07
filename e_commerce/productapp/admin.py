from django.contrib import admin
from .models import wishlist,Coupon,UserCoupon,OrderProduct,Order,CartItem


# Register your models here.
admin.site.register(wishlist)
admin.site.register(Coupon)
admin.site.register(UserCoupon)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(CartItem)





