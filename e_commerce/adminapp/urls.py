from . import views
from django.urls import path



urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),
    path('bases/',views.bases,name='bases'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),

    path('admindashboard/',views.admindashboard,name='admindashboard'),

    path('addcategory/',views.addcategory,name='addcategory'),
    path('viewcategory/',views.viewcategory,name='viewcategory'),
    path('editcategory/<int:pid>/',views.editcategory,name='editcategory'),
    path('deletecategory/<int:pid>/',views.deletecategory,name='deletecategory'),

    path('addproduct/',views.addproduct,name="addproduct"),
    path('viewproduct/',views.viewproduct,name="viewproduct"),
    path('editproduct/<int:pid>/',views.editproduct,name="editproduct"),
    path('deleteproduct/<int:pid>/',views.deleteproduct,name="deleteproduct"),
    
    path('view_coupons',views.view_coupons,name="view_coupons"),
    path('add_coupons',views.add_coupons,name="add_coupons"),
    path('delete_coupon/<int:pid>/',views.delete_coupon,name='delete_coupon'),
    path('edit_coupon/<int:pid>/',views.edit_coupon,name='edit_coupon'),
    
    path('manageuser',views.manageuser,name="manageuser"),
    path('blockuser/<int:id>/',views.blockuser,name="blockuser"),

    path('addvarient/',views.addvarient,name='addvarient'),
    path('viewvarient/',views.viewvarient,name='viewvarient'),
    path('editvarient/<int:id>/',views.editvarient,name='editvarient'),
    path('dltvarient/<int:id>/',views.deleteverient,name='dltvarient'),
    
    path('manage_order/', views.manage_order, name="manage_order"),
    path('update_order/<int:id>/', views.update_order, name="update_order"),

    path('addbanner', views.addbanner, name="addbanner"),
    path('editbanner/<int:pid>/', views.editbanner, name="editbanner"),
    path('viewbanner/', views.viewbanner, name="viewbanner"),
    path('deletebanner/<int:pid>/', views.deletebanner, name="deletebanner"),












]