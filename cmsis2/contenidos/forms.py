from django import forms
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