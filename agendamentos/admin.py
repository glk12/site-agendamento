from django.contrib import admin
from .models import Servico, Profissional, Agendamento

# Register your models here.
admin.site.register(Servico)
admin.site.register(Profissional)
admin.site.register(Agendamento)