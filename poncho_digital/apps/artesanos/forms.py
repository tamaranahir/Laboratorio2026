from django import forms
from django.core.exceptions import ValidationError
from .models import Artesano, Stand, Rubro, Consulta

# ARTESANO

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
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pérez Juan',
                'required': 'required'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 45678901',
                'maxlength': '8',
                'inputmode': 'numeric',
                'pattern': '[1-9]{8}',
                'title': 'El DNI debe contener exactamente 8 dígitos numéricos',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
                'required': 'required'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 3834123456',
                'required': 'required'
            }),
            'provincia': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'localidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad / Departamento',
                'required': 'required'
            }),
            'nombre_marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la marca o emprendimiento'
            }),
            'rubro': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'descripcion_artesanias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describí brevemente los procesos de elaboración, materiales y si utilizás materia prima regional.',
                'required': 'required'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rubro'].empty_label = "-- Seleccione un rubro --"
        self.fields['nombre_marca'].required = True

    # 1. Validación del DNI
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            dni = str(dni).strip()
            if not dni.isdigit():
                raise ValidationError("El DNI debe contener únicamente dígitos numéricos (sin puntos ni espacios).")
            if len(dni) != 8:
                raise ValidationError("El DNI debe contener exactamente 8 dígitos.")

            # Verifica si ya existe una postulación con este DNI (al crear un registro nuevo)
            if not self.instance.pk and Artesano.objects.filter(dni=dni).exists():
                raise ValidationError("Ya existe una postulación registrada con este número de DNI.")
        return dni

    # 2. Validación de telefono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            telefono_limpio = str(telefono).strip().replace('-', '').replace(' ', '').replace('+', '')
            if not telefono_limpio.isdigit():
                raise ValidationError("El teléfono solo puede contener números, espacios o guiones.")
            if len(telefono_limpio) < 8 or len(telefono_limpio) > 15:
                raise ValidationError("Ingrese un número de teléfono válido (entre 8 y 15 dígitos).")
        return telefono

# ADMINISTRADOR

# Formulario de asignación
class StandForm(forms.ModelForm):
    class Meta:
        model = Stand
        fields = ['artesano']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 101'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pabellón A - Textiles'}),
            'artesano': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar únicamente artesanos con postulación aprobada
        self.fields['artesano'].queryset = Artesano.objects.filter(estado_postulacion='aprobado')
        self.fields['artesano'].empty_label = "-- Seleccionar Artesano --"

    def clean_artesano(self):
        artesano = self.cleaned_data.get('artesano')
        if artesano:
            query = Stand.objects.filter(artesano=artesano)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise ValidationError("Este artesano ya tiene un stand asignado en la feria.")
        return artesano

class RubroForm(forms.ModelForm):
    class Meta:
        model = Rubro
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Textil, Gastronomía'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del rubro'}),
        }

# VISITANTE

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['asunto', 'mensaje']
        widgets = {
            'asunto': forms.Select(attrs={'class': 'form-select'}),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escriba aquí su duda sobre precios, stock, personalización...'
            }),
        }

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['respuesta']
        widgets = {
            'respuesta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escriba aquí la respuesta oficial para el usuario...'
            }),
        }