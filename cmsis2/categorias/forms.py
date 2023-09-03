from django import forms
from .models import Categoria, Subcategoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'is_active']
        # widgets = {
        #     'permissions': forms.CheckboxSelectMultiple,  # Use CheckboxSelectMultiple widget
        # }

class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre', 'categoria', 'is_active']
        # widgets = {
        #     'permissions': forms.CheckboxSelectMultiple,  # Use CheckboxSelectMultiple widget
        # }