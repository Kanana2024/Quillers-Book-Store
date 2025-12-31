from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from datetime import date
from .forms import RegisterForm, InquiryForm
from .models import ( Book, Customer, Order, OrderDetail, Branch)

# Helpers
def get_logged_in_customer(request):
    custid = request.session.get('customer_id')
    if not custid:
        return None
    return get_object_or_404(Customer, custid=custid)




# Cart Views
'''
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
'''

def add_to_cart(request, book_id):
    if request.method != "POST":
        return redirect("books")

    cart = request.session.get("cart", {})

    book = get_object_or_404(Book, bookid=book_id)
    book_id = str(book.bookid)

    cart[book_id] = cart.get(book_id, 0) + 1

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(request, f"{book.booktitle} added to cart.")
    return redirect("cart")
def cart_view(request):
    cart = request.session.get("cart", {})
    books = Book.objects.filter(bookid__in=cart.keys())

    cart_items = []
    total = 0

    for book in books:
        qty = cart[str(book.bookid)]
        subtotal = book.price * qty
        total += subtotal

        cart_items.append({
            "book": book,
            "quantity": qty,
            "subtotal": subtotal
        })

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })
def remove_from_cart(request, book_id):
    customer = get_logged_in_customer(request)
    if not customer:
        messages.error(request, "Please log in to manage your cart.")
        return redirect("login")

    cart = request.session.get("cart", {})
    book_id = str(book_id)

    if book_id in cart:
        del cart[book_id]
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in cart.")

    return redirect("cart")
def clear_cart(request):
    customer = get_logged_in_customer(request)
    if not customer:
        messages.error(request, "Please log in to manage your cart.")
        return redirect("login")

    request.session["cart"] = {}
    request.session.modified = True
    messages.success(request, "Cart cleared.")
    return redirect("cart")

'''
def require_customer(request):
    customer = get_logged_in_customer(request)
    if not customer:
        messages.error(request, "Please log in to proceed to checkout.")
        return None
    return customer
'''

def checkout(request):
    customer = get_logged_in_customer(request)
    if not customer:
        messages.error(request, "Please log in to proceed to checkout.")
        return redirect("login")

    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    books = Book.objects.filter(bookid__in=cart.keys())

    total = sum(book.price * cart[str(book.bookid)] for book in books)

    # ONLY place order when form is submitted
    if request.method == "POST":
        branch = Branch.objects.first()

        order = Order.objects.create(
            orderdate=date.today(),
            totalamount=total,
            orderstatus="Pending",
            deliveryaddress=request.POST.get("address"),
            branch=branch,
            customer=customer
        )

        for book in books:
            qty = cart[str(book.bookid)]

            OrderDetail.objects.create(
                order=order,
                book=book,
                booktitle=book.booktitle,
                quantity=qty,
                price=book.price
            )

            book.stockavailable -= qty
            book.save()

        del request.session["cart"]
        request.session.modified = True
        messages.success(request, "Order placed successfully.")
        return redirect("cart")

    # GET request just shows checkout page
    return render(request, "checkout.html", {
        "books": books,
        "cart": cart,
        "total": total
    })



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
