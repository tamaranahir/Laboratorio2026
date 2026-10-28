from django import forms
from .models import Artesano, Stand

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


    #-----------------------------------------------------------
    #ASIGNACION DE STAND
class StandForm(forms.ModelForm):
    class Meta:
        model = Stand
        fields = ['numero', 'ubicacion', 'estado', 'artesano']
        widgets = {'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 105'}),
               'ubicacion': forms.TextInput(
                   attrs={'class': 'form-control', 'placeholder': 'Ej: Pabellón Textil - Sector A'}),
               'estado': forms.Select(attrs={'class': 'form-select'}),
               'artesano': forms.Select(attrs={'class': 'form-select'}),
            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1. Filtramos para que solo aparezcan los artesanos cuyo estado sea 'aprobado'
        self.fields['artesano'].queryset = Artesano.objects.filter(estado_postulacion='aprobado')
        self.fields['artesano'].empty_label = "-- Seleccionar Artesano Aprobado --"

    def clean_artesano(self):
        artesano = self.cleaned_data.get('artesano')
        if artesano:
            # Verificamos si este artesano ya posee un stand asignado
            query = Stand.objects.filter(artesano=artesano)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)

            if query.exists():
                raise forms.ValidationError(
                    "La operación no se realizó porque este artesano ya tiene un stand asignado.")
        return artesano

