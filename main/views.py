from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterForm
from django.shortcuts import render
from .models import Book
from django.db.models import Q
from .forms import InquiryForm
from .models import Customer
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'customersignup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('custpassword')

        try:
            customer = Customer.objects.get(email=email, custpassword=password)
            request.session['customer_id'] = customer.custid
            request.session['customer_name'] = customer.custname
            messages.success(request, f"Welcome back, {customer.custname}!")
            return redirect('home')
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'customerlogin.html')

def inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'index.html', {'success': True})
    else:
        form = InquiryForm()
    return render(request, 'index.html', {'form': form})

 #This view displays your home page
def index(request):
    return render(request, 'index.html')
#View displays about us page
def about(request):
    return render(request, 'about.html')
#Books view
def books(request):
    return render(request, 'books.html')
#Authors view
def authors(request):
    return render(request, 'authors.html')
#Book results
def book_search(request):
    query = request.GET.get('q', '')
    books = []

    if query:
        books = Book.objects.filter(
            Q(booktitle__icontains=query) |
            Q(genre__icontains=query) |
            Q(author__fname__icontains=query) |
            Q(author__lname__icontains=query)
        )
    else:
        books = Book.objects.all()

    return render(request, 'book_results.html', {'books': books, 'query': query})

#Inquiry form 
def contact(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your inquiry has been received. Thank you!')
            return redirect('home') 
    else:
        form = InquiryForm()

    return render(request, 'index.html', {'form': form})