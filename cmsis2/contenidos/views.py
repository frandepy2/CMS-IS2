from django.shortcuts import render, redirect
from .forms import ContenidoForm


# Create your views here.
def crear_contenido(request):
    if request.method == 'POST':
        form = ContenidoForm(request.POST)
        if form.is_valid():
            contenido = form.save(commit=False)  # No guardes el objeto en la base de datos todavía
            if request.user.is_authenticated:
                contenido.autor = request.user  # Asigna el usuario autenticado como autor del contenido
                contenido.estado = 'CREATED'
                contenido.save()  # Guarda el objeto en la base de datos
                return redirect('home')
    else:
        form = ContenidoForm()

    return render(request, 'contenidos/crear_contenido.html', {'form': form})
