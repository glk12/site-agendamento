from django.urls import path
from . import views

urlpatterns = [
    path('novo/', views.agendar_servico, name='agendar_servico'),
    path('sucesso/', views.agendamento_sucesso, name='agendamento_sucesso'),
]
