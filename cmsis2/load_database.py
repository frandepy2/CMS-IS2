from roles.models import CustomPermission
from django.core import management

if not CustomPermission.objects.exists():
    print("Inicia el proceso de carga de datos")
    management.call_command('loaddata', 'databasedump.json')
    print("Finaliza el proceso de carga de datos")
else:
    print("Existen permisos o no se pudo acceder a la carga de datos")