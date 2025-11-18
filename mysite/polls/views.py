from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.db import IntegrityError
from datetime import datetime
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import EmailUserCreationForm, EmailAuthenticationForm, AppointmentForm
from django.contrib import messages
from .models import Service, Professional, Appointment

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
            # autentica automaticamente após registrar
            auth_login(request, user)
            return redirect("index")
    else:
        form = EmailUserCreationForm()
    return render(request, 'register.html', {"form": form})

@login_required(login_url='login')
def agendar(request):
    # Garantir que existam dados básicos (pode ser removido quando usar admin/fixtures)
    if not Service.objects.exists():
        Service.objects.bulk_create([
            Service(name="Corte de Cabelo", duration_minutes=30, price=30),
            Service(name="Barba", duration_minutes=20, price=20),
            Service(name="Sobrancelha", duration_minutes=15, price=15),
            Service(name="Hidratação", duration_minutes=45, price=40),
        ])
    if not Professional.objects.exists():
        Professional.objects.bulk_create([
            Professional(name="João Silva", specialty="Barbeiro Master"),
            Professional(name="Pedro Santos", specialty="Especialista em Cortes"),
            Professional(name="Carlos Lima", specialty="Colorista"),
        ])

    # Suporte a requisições AJAX do front atual (sem alterar UI)
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        service_name = request.POST.get("service_name")
        professional_name = request.POST.get("professional_name")
        date_str = request.POST.get("date")
        time_str = request.POST.get("time")
        notes = request.POST.get("notes", "")

        if not all([service_name, professional_name, date_str, time_str]):
            return JsonResponse({"ok": False, "error": "Dados incompletos."}, status=400)

        try:
            service = Service.objects.get(name=service_name)
        except Service.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Serviço inválido."}, status=400)

        try:
            professional = Professional.objects.get(name=professional_name)
        except Professional.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Profissional inválido."}, status=400)

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            time_obj = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return JsonResponse({"ok": False, "error": "Data ou horário inválidos."}, status=400)

        appointment = Appointment(
            user=request.user,
            service=service,
            professional=professional,
            date=date_obj,
            time=time_obj,
            notes=notes,
        )
        try:
            appointment.save()
        except IntegrityError as e:
            if "unique_professional_slot" in str(e):
                return JsonResponse({"ok": False, "error": "Este profissional já possui um agendamento neste horário."}, status=409)
            return JsonResponse({"ok": False, "error": "Não foi possível salvar o agendamento."}, status=500)

        return JsonResponse({"ok": True}, status=201)

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment: Appointment = form.save(commit=False)
            appointment.user = request.user
            try:
                appointment.save()
            except Exception as e:
                if "unique_professional_slot" in str(e):
                    messages.error(request, "Este profissional já possui um agendamento neste horário.")
                else:
                    messages.error(request, "Não foi possível salvar o agendamento. Tente novamente.")
            else:
                messages.success(request, "Agendamento criado com sucesso!")
                return redirect("meus_agendamentos")
    else:
        form = AppointmentForm()
    return render(request, 'agendar.html', {"form": form})

def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
    return redirect('index')


@login_required(login_url='login')
def meus_agendamentos(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'meus_agendamentos.html', {"appointments": appointments})
