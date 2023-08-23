from django.test import TestCase
from django.contrib.auth import get_user_model

class UsuarioTestCase(TestCase):
    def test_crear_usuario(self):
        Usuario = get_user_model()
        user = Usuario.objects.create_user(email = 'usuario@gmail.com', password='password')
        self.assertEquals(user.email,'usuario@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            Usuario.objects.create_user()

    def test_usuario_subscriptor(self):
        Usuario = get_user_model()
        user = Usuario.objects.create_user(email = 'usuario@gmail.com', password='password')
        self.assertTrue(user.subscribed)

    def test_crear_administrador(self):
        Usuario = get_user_model()
        user = Usuario.objects.create_admin(email = 'usuario@gmail.com', password='password')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    def test_primer_usuario_admin(self):
        Usuario = get_user_model()
        Usuario.objects.all().delete()
        self.assertEqual(Usuario.objects.all().count(), 0,
        "No se pudo limpiar la base de datos")
        Usuario.objects.create_user(email='usuario@gmail.com', password='password')
        self.assertEqual(Usuario.objects.filter(
            groups__name='cms_admin').count(), 1)