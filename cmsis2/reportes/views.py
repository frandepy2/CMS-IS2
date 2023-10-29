from django.shortcuts import render
# Create your views here.
def mostrar_reportes(request):
    return render(request, 'reportes/reportes.html' )
