from django.urls import path
from . import views

# This list holds all the URL patterns (routes) for this app.
urlpatterns = [
    path('customersignup/', views.register, name='register'),
]
