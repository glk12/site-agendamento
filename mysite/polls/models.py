from django.db import models
from django.contrib.auth import get_user_model


class Service(models.Model):
	name = models.CharField(max_length=100)
	duration_minutes = models.PositiveIntegerField(default=30)
	price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return f"{self.name}"


class Professional(models.Model):
	name = models.CharField(max_length=100)
	specialty = models.CharField(max_length=120, blank=True)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return self.name


class Appointment(models.Model):
	STATUS_CHOICES = [
		("scheduled", "Agendado"),
		("completed", "Concluído"),
		("canceled", "Cancelado"),
	]

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="appointments")
	service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="appointments")
	professional = models.ForeignKey(Professional, on_delete=models.PROTECT, related_name="appointments")
	date = models.DateField()
	time = models.TimeField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")
	notes = models.TextField(blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-date", "-time"]
		constraints = [
			models.UniqueConstraint(fields=["professional", "date", "time"], name="unique_professional_slot"),
		]

	def __str__(self) -> str:
		return f"{self.service} com {self.professional} em {self.date} {self.time}"

