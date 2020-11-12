from django.contrib import admin
from django.urls import path,include
from .views import homeview,productdetailview,productview,add_cart,cart,checkout

urlpatterns = [
    
    path('',homeview,name='home'),
    path('products',productview,name='products'),
    path('products/<pk>',productdetailview,name='product'),
    path('addcartitems/<pk>',add_cart,name='addcart'),
    path('cart',cart,name='cart'),
    path('checkout',checkout,name='checkoout')

]
