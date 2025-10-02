from django.urls import path
from . import views

urlpatterns = [
    path('media-profissional/', views.media_por_profissional, name='media_por_profissional'),
]
