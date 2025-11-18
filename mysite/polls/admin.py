from django.contrib import admin
from .models import Service, Professional, Appointment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ("name", "duration_minutes", "price")
	search_fields = ("name",)


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
	list_display = ("name", "specialty")
	search_fields = ("name", "specialty")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	list_display = ("user", "service", "professional", "date", "time", "status")
	list_filter = ("status", "date", "professional", "service")
	search_fields = ("user__username", "user__first_name", "professional__name")

# Register your models here.
