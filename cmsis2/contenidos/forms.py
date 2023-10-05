from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Plantilla, Contenido
from django_quill.forms import QuillFormField
from categorias.models import Subcategoria


class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        cuerpo = QuillFormField()
        fields = ['nombre', 'cuerpo', 'subcategoria']

    def __init__(self, *args, **kwargs):
        categoria_id = kwargs.pop('categoria_id', None)  # Obtén el ID de la categoría específica
        super(ContenidoForm, self).__init__(*args, **kwargs)

        # Filtra el queryset del campo 'subcategoria' para mostrar solo las subcategorías de la categoría específica
        if categoria_id:
            self.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoria_id=categoria_id)


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