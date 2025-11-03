from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import EmailUserCreationForm, EmailAuthenticationForm

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("index")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {"form": form})

def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("index")
    else:
        form = EmailUserCreationForm()
    return render(request, 'register.html', {"form": form})

def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('index')
    return redirect('index')
