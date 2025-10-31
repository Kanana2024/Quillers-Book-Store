from django import forms       # Import Django's forms module for creating forms
from .models import Customer   # Import the Customer model you defined earlier

# This form is linked to the Customer model and is used for user registration.
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['custname', 'email', 'mobile', 'dob', 'gender', 'custpassword']
        widgets = {
            'custpassword': forms.PasswordInput()  # Hides password input with dots or asterisks for security
        }
