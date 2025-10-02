from django.db import models

# Create your models here.

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Profissional(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    cliente = models.CharField(max_length=100)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cliente} - {self.data} {self.hora}"
