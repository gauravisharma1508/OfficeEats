"""cafe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.urls import path
from . import views
from .views import Register,Signin,Signup,Preview,Dish,Cat,Search,Cart,CheckOut,OrderView,logout,Index

urlpatterns = [
    path('',Signin.as_view() , name='signin'),
    path('signin',Signin.as_view() , name='signin'),
    path('register',Register.as_view() , name='register'),
    path('signup',Signup.as_view() , name='signup'),
    path('index',Index.as_view() , name='index'),
    path('preview',Preview.as_view(),name='preview'),
    path('menu',Dish.as_view(),name='menu'),
    path('category/<int:pk>/',Cat.as_view(),name='category'),
    path('category',Cat.as_view(),name='category'),
    path('cart',Cart.as_view(),name='cart'),
    path('checkout',CheckOut.as_view(),name='checkout'),
    path('order',OrderView.as_view(),name='order'),
    path('logout',logout,name='logout'),
    
]
