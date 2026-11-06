from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroClienteForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. cliente1'
        }),
        help_text="Requerido. Solo letras, números y @/./+/-/)."
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresá tu contraseña'
        }),
        help_text="Debe contener al menos 8 caracteres y no ser una contraseña muy común."
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repetí tu contraseña'
        }),
        help_text="Ingresá exactamente la misma contraseña que arriba."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)