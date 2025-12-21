from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

from .forms import RegisterForm, InquiryForm
from .models import (
    Book,
    Customer,
    Cart,
    CartItem
)

# Helpers
def get_logged_in_customer(request):
    custid = request.session.get('customer_id')
    if not custid:
        return None
    return get_object_or_404(Customer, custid=custid)


def get_cart(customer):
    cart, created = Cart.objects.get_or_create(customer=customer)
    return cart

# Cart Views

def add_to_cart(request, book_id):
    if request.method != 'POST':
        return redirect('books')

    customer = get_logged_in_customer(request)
    if not customer:
        messages.error(request, "Please log in to add items to cart.")
        return redirect('login')

    book = get_object_or_404(Book, bookid=book_id)
    cart = get_cart(customer)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book
    )

    if not created:
        item.quantity += 1

    item.save()
    messages.success(request, f"{book.booktitle} added to cart.")

    return redirect('cart')


def cart_view(request):
    customer = get_logged_in_customer(request)
    if not customer:
        messages.error(request, "Please log in to view your cart.")
        return redirect('login')

    cart = get_cart(customer)
    return render(request, 'cart.html', {'cart': cart})

# Authentication

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


def logout_view(request):
    request.session.flush()
    messages.success(request, "You've been logged out successfully!")
    return redirect('home')

# Pages

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})


def authors(request):
    return render(request, 'authors.html')

# Search

def book_search(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(booktitle__icontains=query) |
            Q(genre__icontains=query) |
            Q(author__fname__icontains=query) |
            Q(author__lname__icontains=query)
        )

    return render(request, 'book_results.html', {
        'books': books,
        'query': query
    })

# Inquiry

def inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your inquiry has been received.')
            return redirect('home')
    else:
        form = InquiryForm()

    return render(request, 'index.html', {'form': form})


def contact(request):
    return inquiry(request)
