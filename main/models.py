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
         # db_table defines the exact name of the table in your database
        db_table = 'customer'

    def __str__(self):
        # Defines how the object will be displayed (e.g., in Django admin)
        return self.custname

