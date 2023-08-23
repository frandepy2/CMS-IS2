from django.contrib import admin
from .models import Usuario

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined', 'subscribed')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')

admin.site.register(Usuario,UsuarioAdmin)