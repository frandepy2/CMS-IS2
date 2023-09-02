from django.test import TestCase
from roles.models import CustomRole, CustomPermission, RolePermission, UserCategoryRole
from cmsis2.templatetags.permissions_tags import has_permission, has_category_permission
from usuarios.models import Usuario
from categorias.models import Categoria


class HasPermissionFilterTestCase(TestCase):
    def setUp(self):
        # Crea el rol de ADMIN
        CustomRole.objects.get_or_create(name='Admin', is_system_role=True)
        # Crea un CustomPermission
        self.permission = CustomPermission.objects.create(name='permission_to_test', description='Test permission')

        # Crea un CustomRole con el permiso
        self.role = CustomRole.objects.create(name='test_role')
        RolePermission.objects.create(role=self.role, permission=self.permission)

        # Crea un usuario personalizado y asigna el rol al usuario
        self.user = Usuario.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_category_role = UserCategoryRole.objects.create(user=self.user, role=self.role)

    def test_has_permission_filter_with_permission(self):
        # Prueba el filtro con un permiso que el usuario tiene
        self.assertTrue(has_permission(self.user, 'permission_to_test'))

    def test_has_permission_filter_without_permission(self):
        # Prueba el filtro con un permiso que el usuario no tiene
        self.assertFalse(has_permission(self.user, 'another_permission'))

    def test_has_permission_filter_with_invalid_user(self):
        # Prueba el filtro con un usuario inválido
        invalid_user = Usuario(username='invalid_user', email='invalid@example.com')
        self.assertFalse(has_permission(invalid_user, 'permission_to_test'))

    def test_has_permission_filter_with_empty_permission(self):
        # Prueba el filtro con una cadena de permiso vacía
        self.assertFalse(has_permission(self.user, ''))

    def test_has_permission_filter_with_none_permission(self):
        # Prueba el filtro con un permiso nulo
        self.assertFalse(has_permission(self.user, None))


class CategoryPermissionTest(TestCase):

    def setUp(self):
        # Configuración de datos de prueba
        self.user = Usuario.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.category = Categoria.objects.create(nombre='Test Category')
        self.permission = CustomPermission.objects.create(name='view_category', description='View Category')
        self.role = CustomRole.objects.create(name='category_role')
        self.role.permissions.add(self.permission)
        self.user_category_role = UserCategoryRole.objects.create(user=self.user, category=self.category, role=self.role)

    def test_has_category_permission(self):
        # Verifica si el usuario tiene el permiso para ver la categoría
        has_permission = has_category_permission(self.user, self.category.id, 'view_category')
        self.assertTrue(has_permission)

    def test_no_category_permission(self):
        # Verifica si el usuario NO tiene el permiso para ver la categoría
        has_permission = has_category_permission(self.user, self.category.id, 'other_permission')
        self.assertFalse(has_permission)

    def test_user_not_in_category(self):
        # Verifica si el usuario NO está asociado a la categoría
        other_category = Categoria.objects.create(nombre='Other Category')
        has_permission = has_category_permission(self.user, other_category.id, 'view_category')
        self.assertFalse(has_permission)