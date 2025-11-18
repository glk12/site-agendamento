from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Appointment


def _normalize_phone(phone: str) -> str:
	return "".join(ch for ch in (phone or "") if ch.isdigit())


class PhoneUserCreationForm(UserCreationForm):
	name = forms.CharField(required=True, label="Nome completo")
	phone = forms.CharField(required=True, label="Celular")

	class Meta:
		model = User
		# Apenas campos do modelo User; os extras (name/phone) são tratados manualmente
		fields = ("password1", "password2")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite seu nome completo'})
		self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': '(11) 91234-5678'})
		self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite sua senha'})
		self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme sua senha'})

	def clean_phone(self):
		raw = self.cleaned_data.get("phone", "")
		phone = _normalize_phone(raw)
		if len(phone) < 10:  # mínimo básico (fixo + móvel)
			raise forms.ValidationError("Informe um celular válido.")
		# username é único -> usamos o telefone como username
		if User.objects.filter(username__iexact=phone).exists():
			raise forms.ValidationError("Este celular já está em uso.")
		return phone

	def save(self, commit=True):
		user = super().save(commit=False)
		user.username = self.cleaned_data["phone"]  # armazenamos o telefone normalizado como username
		user.first_name = self.cleaned_data.get("name", "")
		# user.email opcional
		if commit:
			user.save()
		return user


class PhoneAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Celular",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu celular (somente números)",
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


