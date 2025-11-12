from django import forms       # Import Django's forms module for creating forms
from .models import Customer   # Import the Customer model you defined earlier
from .models import Inquiry

# This form is linked to the Customer model and is used for user registration.
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['custname', 'email', 'mobile', 'dob', 'gender', 'custpassword']
        widgets = {
            'custpassword': forms.PasswordInput()  # Hides password input with dots or asterisks for security
        }

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['inqname', 'email', 'inqsubject', 'message']
        widgets = {
            'inqname': forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'form-control'}),
            'inqsubject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Type your message here...', 'class': 'form-control'}),
        }
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=40)
    custpassword = forms.CharField(label="Password", widget=forms.PasswordInput)