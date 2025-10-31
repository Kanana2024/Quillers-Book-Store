from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return HttpResponse("Registered successfully!")  # ✅ only one return
            # return redirect('login')  # 🔒 uncomment later when login works
    else:
        form = RegisterForm()

    return render(request, 'customersignup.html', {'form': form})
 