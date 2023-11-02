from django.test import TestCase
from roles.models import CustomRole, CustomPermission, RolePermission, UserCategoryRole
from usuarios.models import Usuario
from .models import Parametro
from django.urls import reverse
# Create your tests here.
class ParametrosTestCase(TestCase):
    def setUp(self):
        # Crea el rol de Admin
        CustomRole.objects.get_or_create(name='Admin', is_system_role=True)
        # Crea un CustomRole con el permiso
        self.role = CustomRole.objects.create(name='test_role')
        # Crea un CustomPermission
        self.permission = CustomPermission.objects.create(name='manage_parameters', description='Manage Parameters')
        #Asignamos el permiso a Admin
        RolePermission.objects.create(role=self.role, permission=self.permission)

        self.first_user = Usuario.objects.create_user(username='testadmin',
                                                      email='testadmin@gmail.com',
                                                      password='test1password')

        self.user_category_role = UserCategoryRole.objects.create(user=self.first_user, role=self.role)

        # Crea un parámetro de prueba para la cantidad máxima de denuncias
        self.parametro = Parametro.objects.create(clave='MAX_CANT_DENUNCIAS', valor='3')

        #USUARIO SIN PERMISO
        self.user = Usuario.objects.create_user(username='testuser', email='test@example.com', password='testpassword')


    def test_usuario_con_permiso(self):
        """
        Prueba que un cliente tenga acceso de administrador para ver y administrar parametros
        :return:
        """
        self.client.login(username='testadmin', password='test1password')
        response = self.client.get(reverse('lista_y_editar_parametros'))
        self.assertEqual(response.status_code, 200)


    def test_usuario_sin_permiso(self):
        """
        Prueba que un cliente que no tenga acceso de administrador sea redirigido y no pueda hacer nada
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('lista_y_editar_parametros'))
        self.assertEqual(response.status_code, 302)

