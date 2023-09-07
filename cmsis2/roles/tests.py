from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from roles.models import CustomRole, CustomPermission, RolePermission, UserCategoryRole
from cmsis2.templatetags.permissions_tags import has_permission, has_category_permission
from usuarios.models import Usuario
from categorias.models import Categoria
from functools import wraps
from decorators import has_permission_decorator, has_category_permission_decorator


class HasPermissionFilterTestCase(TestCase):
    """
    Pruebas unitarias para el filtro de permisos.

    Estas pruebas evalúan el comportamiento del filtro de permisos en diferentes escenarios.
    """

    def setUp(self):
        """
        Configuración inicial para las pruebas.

        Crea roles, permisos, usuarios y asigna permisos a usuarios para realizar las pruebas.
        """

        # Crea el rol de ADMIN
        CustomRole.objects.get_or_create(name='Admin', is_system_role=True)
        # Crea un CustomPermission
        self.permission = CustomPermission.objects.create(name='permission_to_test', description='Test permission')

        # Crea un CustomRole con el permiso
        self.role = CustomRole.objects.create(name='test_role')
        RolePermission.objects.create(role=self.role, permission=self.permission)

        # Crea un usuario personalizado y asigna el rol al usuario
        self.superuser = Usuario.objects.create_user(username='testAdmin', email='testAdmin@example.com', password='testpassword')

        # Crea un usuario personalizado y asigna el rol al usuario
        self.user = Usuario.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_category_role = UserCategoryRole.objects.create(user=self.user, role=self.role)

    def test_has_permission_filter_with_permission(self):
        """
        Prueba el filtro con un permiso que el usuario tiene.

        Debería retornar True ya que el usuario tiene el permiso 'permission_to_test'.
        """
        self.assertTrue(has_permission(self.user, 'permission_to_test'))

    def test_has_permission_filter_without_permission(self):
        """
        Prueba el filtro con un permiso que el usuario no tiene.

        Debería retornar False ya que el usuario no tiene el permiso 'another_permission'.
        """
        self.assertFalse(has_permission(self.user, 'another_permission'))

    def test_has_permission_filter_with_invalid_user(self):
        """
        Prueba el filtro con un usuario inválido.

        Debería retornar False ya que el usuario no existe en la base de datos.
        """
        invalid_user = Usuario(username='invalid_user', email='invalid@example.com')
        self.assertFalse(has_permission(invalid_user, 'permission_to_test'))

    def test_has_permission_filter_with_empty_permission(self):
        """
        Prueba el filtro con una cadena de permiso vacía.

        Debería retornar False ya que la cadena de permiso está vacía.
        """
        self.assertFalse(has_permission(self.user, ''))

    def test_has_permission_filter_with_none_permission(self):
        """
        Prueba el filtro con un permiso nulo.

        Debería retornar False ya que el permiso es None.
        """
        self.assertFalse(has_permission(self.user, None))


class CategoryPermissionTest(TestCase):
    """
    Pruebas unitarias para la verificación de permisos de categoría.

    Estas pruebas evalúan la funcionalidad de verificación de permisos de categoría para usuarios.
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas.

        Crea roles, permisos, usuarios, categorías y asigna permisos a usuarios para realizar las pruebas.
        """

        # Crea el rol de ADMIN
        CustomRole.objects.get_or_create(name='Admin', is_system_role=True)

        # Configuración de datos de prueba
        self.user = Usuario.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.category = Categoria.objects.create(nombre='Test Category')
        self.permission = CustomPermission.objects.create(name='view_category', description='View Category')
        self.role = CustomRole.objects.create(name='category_role')
        self.role.permissions.add(self.permission)
        self.user_category_role = UserCategoryRole.objects.create(user=self.user, category=self.category, role=self.role)

    def test_has_category_permission(self):
        """
        Verifica si el usuario tiene el permiso para ver la categoría.

        Debería retornar True ya que el usuario tiene el permiso 'view_category' en la categoría 'Test Category'.
        """
        has_permission = has_category_permission(self.user, self.category.id, 'view_category')
        self.assertTrue(has_permission)

    def test_no_category_permission(self):
        """
        Verifica si el usuario NO tiene el permiso para ver la categoría.

        Debería retornar False ya que el usuario no tiene el permiso 'other_permission'.
        """
        has_permission = has_category_permission(self.user, self.category.id, 'other_permission')
        self.assertFalse(has_permission)

    def test_user_not_in_category(self):
        """
        Verifica si el usuario NO está asociado a la categoría.

        Debería retornar False ya que el usuario no está asociado a la categoría 'Other Category'.
        """
        other_category = Categoria.objects.create(nombre='Other Category')
        has_permission = has_category_permission(self.user, other_category.id, 'view_category')
        self.assertFalse(has_permission)


# Create a custom decorator for testing purposes
def dummy_decorator(view_func):
    """
    Un decorador de prueba que simplemente pasa la llamada a la vista sin modificarla.

    :param view_func: La función de vista original.
    :type view_func: callable
    :return: La función de vista original sin cambios.
    :rtype: callable
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


class PermissionsTest(TestCase):
    def setUp(self):
        # Crea el rol de Admin
        CustomRole.objects.get_or_create(name='Admin', is_system_role=True)

        # Crea un usuario personalizado
        self.user = Usuario.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        # Crea roles y permisos personalizados
        self.role = CustomRole.objects.create(name='Test Role', is_active=True)
        self.permission = CustomPermission.objects.create(name='view_roles', description='Test Description')
        self.role_permission = RolePermission.objects.create(role=self.role, permission=self.permission)

        # Crea un UserCategoryRole para el usuario
        self.user_category_role = UserCategoryRole.objects.create(user=self.user, role=self.role)

        # Crea otro usuario para pruebas adicionales
        self.user = Usuario.objects.create_user(username='testuser2', email='test2@example.com', password='testpassword')

    def test_has_permission_decorator(self):
        """
        Prueba el decorador has_permission_decorator con un usuario que tiene el permiso.
        """
        @has_permission_decorator('view_roles')
        @dummy_decorator
        def view_with_permission(request):
            return HttpResponse('Permission granted')

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('roles'))
        self.assertEqual(response.status_code, 200)

    def test_has_permission_decorator_no_permission(self):
        """
        Prueba el decorador has_permission_decorator con un usuario que no tiene el permiso.
        """
        @has_permission_decorator('view_roles')
        @dummy_decorator
        def view_without_permission(request):
            return HttpResponse('Permission denied')

        self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse('roles'))
        self.assertEqual(response.status_code, 302)  # Debe ser redirigido

    def test_has_category_permission_decorator(self):
        """
        Prueba el decorador has_category_permission_decorator con un usuario que tiene el permiso en la categoría.
        """
        @has_category_permission_decorator(category_id=1, permission_name='view_roles')
        @dummy_decorator
        def view_with_category_permission(request):
            return HttpResponse('Category permission granted')

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('roles'))
        self.assertEqual(response.status_code, 200)

    def test_has_category_permission_decorator_no_permission(self):
        """
        Prueba el decorador has_category_permission_decorator con un usuario que no tiene el permiso en la categoría.
        """
        # Prueba el decorador has_category_permission_decorator con un usuario que no tiene el permiso en la categoría.
        @has_category_permission_decorator(category_id=1, permission_name='view_roles')
        @dummy_decorator
        def view_without_category_permission(request):
            return HttpResponse('roles')

        self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse('roles'))
        self.assertEqual(response.status_code, 302)  # Debe ser redirigido

    def tearDown(self):
        self.client.logout()
        self.user.delete()
        self.role.delete()
        self.permission.delete()
        self.role_permission.delete()
        self.user_category_role.delete()


