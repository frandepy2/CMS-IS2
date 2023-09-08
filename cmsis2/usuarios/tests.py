from django.test import TestCase
from django.contrib.auth import get_user_model

from roles.models import CustomRole


class UsuarioTestCase(TestCase):
    def setUp(self):
        # Crea el rol de ADMIN
        CustomRole.objects.get_or_create(name='Admin', is_system_role=True)
    def test_crear_usuario(self):
        """
        Prueba la creación de un usuario estándar.

        Se asegura de que un usuario se crea con los atributos correctos.
        """
        Usuario = get_user_model()

        first_user = Usuario.objects.create_user(username = 'user_1', email = 'usuario1@gmail.com', password='password')
        self.assertEquals(first_user.email,'usuario1@gmail.com')
        self.assertTrue(first_user.is_active)
        self.assertTrue(first_user.is_staff)
        self.assertFalse(first_user.is_superuser)

        user = Usuario.objects.create_user(username = 'user_2', email = 'usuario2@gmail.com', password='password')
        self.assertEquals(user.email,'usuario2@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            Usuario.objects.create_user()

    def test_usuario_subscriptor(self):
        """
        Prueba que un usuario se crea como subscriptor.

        Verifica si un usuario se crea con la propiedad `subscribed` como verdadera.
        """
        Usuario = get_user_model()
        user = Usuario.objects.create_user(email = 'usuario@gmail.com', password='password')
        self.assertTrue(user.subscribed)

    def test_crear_administrador(self):
        """
        Prueba la creación de un administrador.

        Verifica si un administrador se crea con los atributos correctos.
        """
        Usuario = get_user_model()
        user = Usuario.objects.create_superuser(email = 'usuario@gmail.com', password='password')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    def test_primer_usuario_admin(self):
        """
        Prueba que se crea un usuario administrador al ser el primer usuario.

        Verifica si se crea un usuario administrador al no haber otros usuarios en la base de datos.
        """
        Usuario = get_user_model()
        Usuario.objects.all().delete()
        self.assertEqual(Usuario.objects.all().count(), 0,
        "No se pudo limpiar la base de datos")
        Usuario.objects.create_user(email='usuario@gmail.com', password='password')
        self.assertEqual(Usuario.objects.filter(
            groups__name='cms_admin').count(), 1)