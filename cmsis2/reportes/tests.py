from django.test import TestCase
from django.urls import reverse

from usuarios.models import Usuario
from roles.models import CustomRole, CustomPermission, RolePermission, UserCategoryRole
from categorias.models import Categoria

# Create your tests here.
class ReporteViewsTestCase(TestCase):
    def setUp(self):
        # Crea el rol de Admin
        CustomRole.objects.get_or_create(name='Admin', is_system_role=True)
        self.first_user = Usuario.objects.create_user(username='testadmin',
                                                      email='testadmin@gmail.com',
                                                      password='test1password')

        # Configura el entorno de prueba, como usuarios, plantillas y contenido

        self.user = Usuario.objects.create_user(username='testuser', email='testuser@gmail.com',
                                                password='testpassword')
        self.custom_permission = CustomPermission(name='view_reports', description='Ver Reportes')
        self.custom_permission.save()

        self.custom_role = CustomRole.objects.create(name='test_role')

        self.role_permission = RolePermission.objects.create(role=self.custom_role, permission=self.custom_permission)

        self.categoria = Categoria.objects.create(nombre='Prueba', descripcion='Categoria de Prueba')

    def test_mostrar_reportes(self):
        """
        Prueba que la vista mostrar reportes se muestre a un usuario con permiso para ver los reportes
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, role=self.custom_role)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mostrar_reportes'))
        self.assertEqual(response.status_code, 200)


    def test_mostrar_reportes_not_logged_in(self):
        """
        Prueba que la vista mostrar reportes redirige a un usuario si es que no ha iniciado sesión.
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, role=self.custom_role)
        response = self.client.get(reverse('mostrar_reportes'))
        self.assertEqual(response.status_code, 302)


    def test_mostrar_reportes_no_permission(self):
        """
        Prueba que la vista mostrar reportes redirige a un usuario si es que no tiene el permiso necesario.
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mostrar_reportes'))
        self.assertEqual(response.status_code, 302)


    def test_mostrar_reportes_por_categoria(self):
        """
        Prueba que la vista mostrar reportes por categoria se muestre a un usuario con permiso para ver los reportes
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, role=self.custom_role)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mostrar_reportes_por_categoria', args=[self.categoria.id]))
        self.assertEqual(response.status_code, 200)


    def test_mostrar_reportes_por_categoria_not_logged_in(self):
        """
        Prueba que la vista mostrar reportes por categoria redirige a un usuario si es que no ha iniciado sesion.
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, role=self.custom_role)
        response = self.client.get(reverse('mostrar_reportes_por_categoria', args=[self.categoria.id]))
        self.assertEqual(response.status_code, 302)


    def test_mostrar_reportes_por_categoria_no_permission(self):
        """
        Prueba que la vista mostrar reportes por categoria redirige a un usuario si es que no tiene el permiso necesario.
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mostrar_reportes_por_categoria', args=[self.categoria.id]))
        self.assertEqual(response.status_code, 302)

