from django import forms
from .models import Artesano

class ArtesanoForm(forms.ModelForm):
    class Meta:
        model = Artesano
        fields = [
            'nombre_completo',
            'dni',
            'email',
            'telefono',
            'provincia',
            'localidad',
            'nombre_marca',
            'rubro',
            'descripcion_artesanias',
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pérez Juan'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de DNI'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp / Teléfono'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad / Departamento'}),
            'nombre_marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de tu marca o emprendimiento'}),
            'rubro': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_artesanias': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describí brevemente tus productos o técnicas'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rubro'].empty_label = "-- Seleccione un rubro --"