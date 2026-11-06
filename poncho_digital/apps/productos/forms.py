from django import forms
from django.core.exceptions import ValidationError
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['categoria', 'nombre', 'descripcion', 'precio', 'stock', 'imagen', 'activo']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select','required': 'required'}),

            'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ej: Poncho Catamarqueño en Hilado Fino','maxlength': '150','required': 'required'}),

            'descripcion': forms.Textarea(attrs={'class': 'form-control','rows': 3,'placeholder': 'Describí las técnicas, tipo de telar y materiales utilizados...','required': 'required'}),

            'precio': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Ej: 15000.00','step': '0.01','min': '0.01','required': 'required'}),

            'stock': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Ej: 5','min': '1','required': 'required'}),

            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control','accept': 'image/*'}),

            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = "-- Seleccionar Categoría --"
        if self.instance and self.instance.pk:
            self.fields['imagen'].required = False
        else:
            self.fields['imagen'].required = True

    # 1. Validación de precio (Debe ser mayor a 0)
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise ValidationError("El precio de venta debe ser un monto mayor a $0,00.")
        return precio

    # 2. Validación de stock (Mínimo 1 unidad)
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 1:
            raise ValidationError("La cantidad de stock inicial debe ser de al menos 1 unidad.")
        return stock

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Textiles, Cerámica'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la categoría'}),
        }