from django import forms
from .models import Artesano

class ArtesanoForm(forms.ModelForm):
    class Meta:
        model = Artesano
        # Campos que completará el postulante
        fields = [
            'nombre_completo',
            'dni',
            'email',
            'telefono',
            'provincia',
            'departamento',
            'nombre_marca',
            'rubro',
            'descripcion_tecnicas',
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba su nombre completo'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 45678901'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'usuario@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3834123456'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Catamarca'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departamento'}),
            'nombre_marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Tejidos El Poncho'}),
            'rubro': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_tecnicas': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describa brevemente sus técnicas y materiales...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rubro'].empty_label = "-- Seleccione un rubro --"