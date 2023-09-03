from django import forms
from .models import CustomRole, UserCategoryRole, CustomPermission
from usuarios.models import Usuario
from categorias.models import Categoria

class CustomRoleForm(forms.ModelForm):
    class Meta:
        model = CustomRole
        fields = ['name',  'permissions', 'is_system_role']
        widgets = {
            'permissions': forms.CheckboxSelectMultiple,  # Use CheckboxSelectMultiple widget
        }

    def clean(self):
        cleaned_data = super().clean()
        is_system_role = cleaned_data.get('is_system_role', False)
        permissions = cleaned_data.get('permissions')

        if is_system_role and permissions:
            non_system_permissions = permissions.filter(is_system_permission=False)
            if non_system_permissions:
                raise forms.ValidationError("No puedes asignar permisos que no son del sistema")

        if not is_system_role and permissions:
            system_permissions = permissions.filter(is_system_permission=True)
            if system_permissions:
                raise forms.ValidationError("No puedes asignar permisos que son del sistema")

        return cleaned_data


class UserCategoryRoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
            self.fields['user'].widget.attrs['disabled'] = True

        self.fields['category'].queryset = Categoria.objects.all()

    user = forms.ModelChoiceField(queryset=Usuario.objects.all(), required=False, disabled=True)
    role = forms.ModelChoiceField(queryset=CustomRole.objects.all(), required=True, empty_label=None, label="Rol")
    category = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False, empty_label="No Category", label="Categoria")

    class Meta:
        model = UserCategoryRole
        fields = ['user', 'role', 'category']

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        category = cleaned_data.get('category')

        if role and role.is_system_role and category:
            raise forms.ValidationError("Category cannot be set for system roles.")

        if role and not role.is_system_role and not category:
            raise forms.ValidationError("Please select a category for this role.")

        if role and role.is_system_role and not category:
            # Check if there is an existing record with the same user and role
            user = cleaned_data.get('user')

            existing_record = UserCategoryRole.objects.filter(user=user, category=None).first()
            if existing_record:
                raise forms.ValidationError("You can not get two system roles")

            existing_record = UserCategoryRole.objects.filter(user=user, role=role).first()

            if existing_record:
                raise forms.ValidationError("A record with the same user and role already exists.")

        if role and not role.is_system_role and category:
            user = cleaned_data.get('user')
            existing_record = UserCategoryRole.objects.filter(user=user, category=category).first()
            if existing_record:
                raise forms.ValidationError("This user have a role in this category already")


        return cleaned_data