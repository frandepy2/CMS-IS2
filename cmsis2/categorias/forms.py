from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'is_active']
        # widgets = {
        #     'permissions': forms.CheckboxSelectMultiple,  # Use CheckboxSelectMultiple widget
        # }