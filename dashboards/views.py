from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from feedbacks.models import Feedback
from agendamentos.models import Profissional
from django.db.models import Avg

def media_por_profissional(request):
    dados = (
        Profissional.objects
        .annotate(media_nota=Avg('agendamento__feedback__nota'))
        .values('nome', 'media_nota')
    )
    nomes = [d['nome'] for d in dados]
    medias = [round(d['media_nota'], 2) if d['media_nota'] else 0 for d in dados]

    context = {
        'nomes': nomes,
        'medias': medias,
    }
    return render(request, 'dashboard/media_por_profissional.html', context)
