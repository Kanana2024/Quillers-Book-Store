from django.contrib import admin
from .models import Customer, Author, Book, Inquiry, Branch, Order, OrderDetail, Staff,SalesReport, InventoryReport, StoreStatistics
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('custname', 'email', 'mobile', 'dob', 'gender')
    search_fields = ('custname', 'email', 'mobile','dob','gender')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'mobile', 'nationality')
    search_fields = ('fname', 'lname', 'email','mobile','nationality')


class BookAdmin(admin.ModelAdmin):
    list_display = ('booktitle', 'author', 'genre', 'price', 'Publicationyear', 'stockavailable')
    search_fields = ('booktitle', 'author__fname', 'author__lname','Publicationyear','stockavailable','price')
    list_filter = ('genre', 'Publicationyear')


class InquiryAdmin(admin.ModelAdmin):
    list_display = ('inqname', 'email', 'inqsubject', 'custid','isread')
    search_fields = ('inqname', 'email', 'inqsubject','isread')
    readonly_fields = ('custid',)
    list_filter = ('isread',)
    list_editable = ('isread',)


class BranchAdmin(admin.ModelAdmin):
    list_display = ('branchname', 'branchlocation', 'branchcountry', 'branchstatus')
    search_fields = ('branchname', 'branchlocation', 'branchcountry','branchstatus')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderid', 'orderdate', 'customer', 'totalamount', 'orderstatus', 'branch')
    list_filter = ('orderstatus', 'orderdate','customer','totalamount','orderstatus','branch')
    search_fields = ('customer__custname', 'branch__branchname')
    readonly_fields = ('orderid','orderdate','customer','totalamount')

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'price', 'paymentdetails')
    search_fields = ('order__orderid', 'book__booktitle', 'paymentdetails')
    readonly_fields = ('order', 'price')
class StaffAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'phone', 'branch', 'staffrole')
    search_fields = ('fullname', 'email', 'staffrole', 'branch__branchname', 'phone')

class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('month', 'total_orders', 'total_sales')
    ordering = ('-month',)
    readonly_fields = ('month', 'total_orders', 'total_sales')

class InventoryReportAdmin(admin.ModelAdmin):
    list_display = ('bookTitle', 'stockLeft')
    ordering = ('bookTitle',)
    readonly_fields = ('bookTitle', 'stockLeft')
class StoreStatisticsAdmin(admin.ModelAdmin):
    list_display = ('totalCustomers', 'totalBooks', 'totalStaff', 'totalOrders', 'totalSales')
    readonly_fields = ('totalCustomers', 'totalBooks', 'totalStaff', 'totalOrders', 'totalSales')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False   
admin.site.site_title = "Quillers Admin Portal"
admin.site.site_header = "Quillers Admin"
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(SalesReport, SalesReportAdmin)
admin.site.register(InventoryReport, InventoryReportAdmin)
admin.site.register(StoreStatistics, StoreStatisticsAdmin)
