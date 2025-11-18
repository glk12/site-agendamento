from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Appointment


class EmailUserCreationForm(UserCreationForm):
	name = forms.CharField(required=True, label="Nome completo")
	email = forms.EmailField(required=True, label="Email")

	class Meta:
		model = User
		# name não é campo do modelo User; mantemos apenas os campos do modelo
		fields = ("email", "password1", "password2")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# adiciona classes/placeholder para ficar compatível com Bootstrap
		self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite seu nome completo'})
		self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite seu email'})
		self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite sua senha'})
		self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme sua senha'})

	def clean_email(self):
		email = self.cleaned_data.get("email")
		if User.objects.filter(email__iexact=email).exists():
			raise forms.ValidationError("Este email já está em uso.")
		return email

	def save(self, commit=True):
		user = super().save(commit=False)
		# mapear campos extras para o User padrão
		user.username = self.cleaned_data["email"]
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data.get("name", "")
		if commit:
			user.save()
		return user


class EmailAuthenticationForm(AuthenticationForm):
	username = forms.EmailField(
		label="Email",
		widget=forms.EmailInput(attrs={
			"class": "form-control",
			"placeholder": "Digite seu email",
			"autofocus": True,
		}),
	)
	password = forms.CharField(
		label="Senha",
		strip=False,
		widget=forms.PasswordInput(attrs={
			"class": "form-control",
			"placeholder": "Digite sua senha",
		}),
	)


class DateInput(forms.DateInput):
	input_type = "date"


class TimeInput(forms.TimeInput):
	input_type = "time"


class AppointmentForm(forms.ModelForm):
	class Meta:
		model = Appointment
		fields = ["service", "professional", "date", "time", "notes"]
		widgets = {
			"service": forms.Select(attrs={"class": "form-control"}),
			"professional": forms.Select(attrs={"class": "form-control"}),
			"date": DateInput(attrs={"class": "form-control"}),
			"time": TimeInput(attrs={"class": "form-control"}),
			"notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Observações (opcional)"}),
		}
		labels = {
			"service": "Serviço",
			"professional": "Profissional",
			"date": "Data",
			"time": "Hora",
			"notes": "Observações",
		}


