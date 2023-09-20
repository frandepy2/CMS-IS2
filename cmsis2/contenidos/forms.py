from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Contenido

class ContenidoForm(forms.ModelForm):
    cuerpo = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Contenido
        fields = ['nombre', 'cuerpo', 'subcategoria']