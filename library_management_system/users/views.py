from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import SignupForm, LoginForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('book_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('book_list')
        messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {"form": form})


def logout_view(request):
    # Allow GET for convenience (avoids 405) and POST (default secure way)
    if request.method in ["GET", "POST"]:
        logout(request)
        messages.info(request, "Logged out.")
        return redirect('login')
    return redirect('book_list')