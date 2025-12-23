'''
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# This list holds all the URL patterns (routes) for this app.
urlpatterns = [
    path('', views.index, name='home'),
    path('about',views.about, name='about'),
    path('books',views.books, name='books'),
    path('customersignup', views.register, name='register'),
    path('customerlogin',views.login, name='login'),
    path('authors.html',views.authors,name='authors'),
    path('books/', views.book_search, name='book_search'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart')
]
'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('about/', views.about, name='about'),

    path('books/', views.books, name='books'),
    path('books/search/', views.book_search, name='book_search'),

    path('authors/', views.authors, name='authors'),

    path('customersignup/', views.register, name='register'),
    path('customerlogin/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    #path('cart/', views.cart_view, name='cart'),
    path("cart/", views.cart_view, name="cart"),
    path("add-to-cart/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:book_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("clear-cart/", views.clear_cart, name="clear_cart"),
    path('inquiry/', views.inquiry, name='inquiry'),
]
