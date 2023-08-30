from django.contrib import admin
from .models import CustomRole, CustomPermission

# Register your models here.

admin.site.register(CustomRole)
admin.site.register(CustomPermission)