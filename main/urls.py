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
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout')
]
