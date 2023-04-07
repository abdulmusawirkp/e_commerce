from django.urls import path
from . import views



urlpatterns = [
    path('', views.base,name='base'),
    path('loginpage/', views.loginpage,name='loginpage'),
    path('register/', views.register,name='register'),
    path('forgotpassword/', views.forgotpassword,name='forgotpassword'),
    path('resetpassword/<int:user_id>/', views.resetpassword,name='resetpassword'),
    path('verify_otp/<int:user_id>/', views.verify_otp,name='verify_otp'),
    path('resend_otp/<int:user_id>/',views.resend_otp,name='resend_otp'),

    path('logout/', views.logout,name='logout'),
    path('userprofile/', views.userprofile,name='userprofile'),
    path('useraddress/',views.address_book,name="useraddress"),
    path('addaddress/<int:id>/',views.add_address,name="add_address"),
    path('updateprofile',views.updateprofile,name="updateuserprofile"),
    path('changepass/',views.changepassword,name="changepassword"),
    path('editaddress/<int:address_id>/', views.edit_address, name='edit_address'),

    path('userproduct/<int:id>/',views.userproduct,name="userproduct"),   
    path('usersingleproduct/<int:id>/',views.usersingleproduct,name="usersingleproduct"),
    path('search/',views.search,name="search"),
    path('myorders/',views.myorders,name='myorders'),
    path('vieworder/<int:id>/',views.viewOrder, name='vieworder'),
    path('cancel-order/<int:id>/',views.cancelOrder, name='cancel_order'),

    

]