from django import forms
from .models import Comentario


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        labels = {
            'texto': 'Agrega tu comentario aqui:',
        }
        widgets ={
            'texto': forms.Textarea(attrs={'class': 'form-control','rows': 2, 'style': 'resize: none;'})
        }