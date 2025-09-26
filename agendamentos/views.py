from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import AgendamentoForm

def agendar_servico(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agendamento_sucesso')
    else:
        form = AgendamentoForm()
    return render(request, 'agendamentos/agendar.html', {'form': form})

def agendamento_sucesso(request):
    return render(request, 'agendamentos/sucesso.html')
