from django.db import models

# Create your models here.
class Feedback(models.Model):
    agendamento = models.OneToOneField('agendamentos.Agendamento', on_delete=models.CASCADE)
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    sentimento = models.CharField(max_length=20, blank=True)
