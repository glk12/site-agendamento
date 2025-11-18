from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
	path("register/", views.register, name = "register"),
    path("agendar/", views.agendar, name="agendar"),
    path("logout/", views.logout_view, name="logout"),
    path("meus-agendamentos/", views.meus_agendamentos, name="meus_agendamentos"),
]
