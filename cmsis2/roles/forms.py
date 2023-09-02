from django import forms
from .models import CustomRole

class CustomRoleForm(forms.ModelForm):
    class Meta:
        model = CustomRole
        fields = ['name',  'permissions', 'is_system_role']
        widgets = {
            'permissions': forms.CheckboxSelectMultiple,  # Use CheckboxSelectMultiple widget
        }
