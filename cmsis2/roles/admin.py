from django.contrib import admin
from .models import CustomRole, CustomPermission,RolePermission,UserCategoryRole

# Register your models here.

admin.site.register(CustomRole)
admin.site.register(CustomPermission)
admin.site.register(RolePermission)
admin.site.register(UserCategoryRole)