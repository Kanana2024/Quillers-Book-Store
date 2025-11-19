from django.db import models

# Create your models here.
# The Customer model represents the structure of customer data stored in the database.
class Customer(models.Model):
    custid = models.AutoField(primary_key=True)
    custname = models.CharField(max_length=50)
    email = models.EmailField(max_length=40, unique=True)
    mobile = models.CharField(max_length=12, unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=6)
    custpassword = models.CharField(max_length=20, unique=True)

    class Meta:
        managed = False
        db_table = 'customer'

    def __str__(self):
        # Defines how the object will be displayed (e.g., in Django admin)
        return self.custname

#Authors model
class Author(models.Model):
    authid = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=40, unique=True)
    mobile = models.CharField(max_length=12, unique=True)
    nationality = models.CharField(max_length=50)

    class Meta:
        managed = False 
        db_table = 'author'

    def __str__(self):
        return f"{self.fname} {self.lname}"


class Book(models.Model):
    bookid = models.AutoField(primary_key=True)
    ISBN = models.CharField(max_length=20, unique=True)
    booktitle = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Publicationyear = models.PositiveSmallIntegerField(null=True, blank=True)
    stockavailable = models.IntegerField(null=True, blank=True)
    bookdescription = models.CharField(max_length=200, null=True, blank=True)
    edition = models.CharField(max_length=20, null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)

    #  Proper ForeignKey link to Author
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        db_column='authid'
    )

    class Meta:
        managed = False
        db_table = 'book'

    def __str__(self):
        return self.booktitle

class Inquiry(models.Model):
    inqid = models.AutoField(primary_key=True)
    inqname = models.CharField(max_length=100)
    email = models.CharField(max_length=20)
    inqsubject = models.CharField(max_length=20)
    message = models.CharField(max_length=100, null=True, blank=True)
    isread = models.BooleanField(default=False)

    
    custid = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        db_column='custid', 
        null=True, blank=True
    )

    class Meta:
        db_table = 'inquiries'
        managed = False

    def __str__(self):
        return f"{self.inqname} - {self.inqsubject}"
    

#BRANCH MODEL
class Branch(models.Model):
    branchid = models.AutoField(primary_key=True)
    branchname = models.CharField(max_length=50, blank=True, null=True)
    branchlocation = models.CharField(max_length=50)
    branchcountry = models.CharField(max_length=50, blank=True, null=True)
    branchstatus = models.CharField(max_length=20, blank=True, null=True)
    branchnumber = models.CharField(max_length=20, blank=True, null=True)
    branchemail = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch'
    def __str__(self):
        return f"{self.branchname} - {self.branchlocation}"



#ORDERS MODEL
class Order(models.Model):
    orderid = models.AutoField(primary_key=True)
    orderdate = models.DateField()
    totalamount = models.DecimalField(max_digits=10, decimal_places=2)
    orderstatus = models.CharField(max_length=20, blank=True, null=True)
    deliveryaddress = models.CharField(max_length=100, blank=True, null=True)
    branch = models.ForeignKey(Branch, db_column='branchid', on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(Customer, db_column='custid', on_delete=models.CASCADE, related_name='orders')

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return f"Order #{self.orderid} - {self.customer}"
 
#ORDER DETAILS MODEL
class OrderDetail(models.Model):
    orderitemid = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,db_column='orderid')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,db_column='bookid')
    booktitle = models.CharField(max_length=100, blank=True, null=True)
    paymentdetails = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'orderdetails'  # Match the exact MySQL table name

    def __str__(self):
        return f"{self.book.booktitle} x{self.quantity} (Order #{self.order.orderid})"

    
#STAFF MODELS   
class Staff(models.Model):
    staffid = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='branchid')
    staffpassword = models.CharField(max_length=20)
    staffrole = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff'

    def __str__(self):
        return f"{self.fullname} ({self.staffrole})"
    
class SalesReport(models.Model):
    month = models.CharField(max_length=7, primary_key=True)
    total_orders = models.IntegerField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'sales_report'
        verbose_name = 'Sales Report'
        verbose_name_plural = 'Sales Report'

    def __str__(self):
        return f"{self.month} - KES {self.total_sales}"

class InventoryReport(models.Model):
    bookTitle = models.CharField(max_length=100, primary_key=True)
    stockLeft = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'inventory_report'
        verbose_name = 'Inventory Report'
        verbose_name_plural = 'Inventory Report'

    def __str__(self):
        return f"{self.bookTitle} ({self.stockLeft} left)"

class StoreStatistics(models.Model):
    id = models.IntegerField(primary_key=True)
    totalCustomers = models.IntegerField()
    totalBooks = models.IntegerField()
    totalStaff = models.IntegerField()
    totalOrders = models.IntegerField()
    totalSales = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False 
        db_table = 'quillerbookstorestatistics'
        verbose_name = "Store Statistic"
        verbose_name_plural = "Store Statistics"

    def __str__(self):
        return "Overall Store Statistics"