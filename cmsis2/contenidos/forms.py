from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Contenido


class ContenidoForm(forms.ModelForm):
    cuerpo = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Contenido
        fields = ['nombre', 'cuerpo', 'subcategoria']


class AprobarContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['fecha_caducidad']

    fecha_caducidad = forms.DateField(
        widget=DatePickerInput(
            options={
                "format": "DD-MM-YYYY",  # Configura el formato de fecha deseado
            },
            attrs={
                "placeholder": "Selecciona la fecha de caducidad",
            }
        ),
        help_text='Selecciona la fecha de caducidad',
    )