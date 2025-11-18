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
    return render(request, 'register.html')
def agendar(request): 
    return render(request, 'polls/agendar.html')
