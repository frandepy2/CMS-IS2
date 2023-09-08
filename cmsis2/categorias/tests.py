from django.test import TestCase, Client
from .models import Categoria, Subcategoria
from .forms import CategoriaForm, SubcategoriaForm
from django.urls import reverse
from usuarios.models import Usuario
from roles.models import CustomRole, CustomPermission, RolePermission, UserCategoryRole

# Create your tests here.
class CategoriaViewTests(TestCase):
    def setUp(self):
        self.adminRole = CustomRole.objects.get_or_create(name='Admin', is_system_role=True)
        self.client = Client()
        self.user = Usuario.objects.create_user(username='user_1', email='usuario1@gmail.com', password='password')
        self.user = Usuario.objects.create_user(username='user_2', email='usuario2@gmail.com', password='password')
        self.permission = CustomPermission.objects.get_or_create(name='view_category', is_system_permission=True)
        self.permission2 = CustomPermission.objects.get_or_create(name='create_category', is_system_permission=True)
        role_permission, created = RolePermission.objects.get_or_create(role=self.adminRole[0], permission=self.permission[0])
        role_permission, created = RolePermission.objects.get_or_create(role=self.adminRole[0], permission=self.permission2[0])
    def test_categorias_view(self):
        """
        Probamos que un solo usuario con permiso de "view_category"
        :return:
        """
        self.client.login(username='user_1', password='password')
        response = self.client.get(reverse('categorias'))
        self.assertEqual(response.status_code, 200)

    def test_categorias_view_not_user_perm(self):
        """
        Probamos que un solo usuario con permiso de "view_category"
        :return:
        """
        self.client.login(username='user_2', password='password')
        response = self.client.get(reverse('categorias'))
        self.assertEqual(response.status_code, 302)


    def test_crear_categoria_view(self):
        """
        Probamos la creacion de una nueva categoria desde la vista
        :return:
        """
        self.client.login(username='user_1', password='password')
        datos_categoria = {
            'nombre': 'Nueva Categoría',
            'descripcion': 'Descripción de la nueva categoría',
            'is_active': True,
        }

        # Realiza una solicitud POST para crear la categoría
        response = self.client.post(reverse('crear_categoria'), data=datos_categoria)

        # Verifica que la categoría se haya creado exitosamente
        self.assertEqual(response.status_code, 302)  # Debería redirigir después de una creación exitosa
        self.assertEqual(Categoria.objects.count(), 1)  # Debería haber una categoría en la base de datos
        nueva_categoria = Categoria.objects.first()
        self.assertEqual(nueva_categoria.nombre, 'Nueva Categoría')  # Verifica el nombre de la categoría
