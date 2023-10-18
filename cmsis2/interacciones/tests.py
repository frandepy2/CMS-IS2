from django.test import TestCase, Client
from django.urls import reverse

from usuarios.models import Usuario
from .models import Comentario, Accion
from roles.models import CustomRole, CustomPermission, RolePermission, UserCategoryRole
from categorias.models import Categoria,Subcategoria
from contenidos.models import Contenido


# Create your tests here.

class ComentarioTestCase(TestCase):
    def setUp(self):
        """
        Configuración inicial para los tests de comentarios.
        Se crea un usuario, categoría, subcategoría y contenido.
        """
        self.client = Client()
        self.user = Usuario.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.categoria = Categoria.objects.create(nombre="TestCategory", descripcion="This is a test category")
        self.subcategoria = Subcategoria.objects.create(nombre="TestSubcategory", categoria=self.categoria)
        self.contenido = Contenido.objects.create(nombre='Test Contenido', cuerpo='{"html":"<p>Prueba de contenido</p>", "delta": {"ops":[{"insert": "Prueba de contenido"}]}}', autor=self.user,
                                                  subcategoria=self.subcategoria, estado='PUBLICADO')


    def test_crear_comentario(self):
        """
        Prueba de creación de un comentario estando autenticado.
        Se espera que el comentario se cree correctamente.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('crear_comentario', args=[self.contenido.id]), {
            'texto': 'This is a test comment',  # assuming your ComentarioForm has a field named 'texto'
        })
        self.assertEqual(response.status_code, 302)
        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.cantidad_comentarios, 1)

    def test_crear_comentario_anonimo(self):
        """
        Prueba de intento de creación de un comentario como usuario anónimo.
        Se espera que el comentario no se cree.
        """
        response = self.client.post(reverse('crear_comentario', args=[self.contenido.id]), {
            'texto': 'This is a test comment',
        })

        self.assertEqual(response.status_code,
                         302)

        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.cantidad_comentarios, 0)  # El comentario no debería haber sido creado

class MeGustaTestCase(TestCase):

    def setUp(self):
        """
        Configuración inicial para los tests de "Me gusta".
        Se crea un usuario, categoría, subcategoría y contenido.
        """
        self.client = Client()
        self.user = Usuario.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.categoria = Categoria.objects.create(nombre="TestCategory", descripcion="This is a test category")
        self.subcategoria = Subcategoria.objects.create(nombre="TestSubcategory", categoria=self.categoria)
        self.contenido = Contenido.objects.create(nombre='Test Contenido', cuerpo='{"html":"<p>Prueba de contenido</p>", "delta": {"ops":[{"insert": "Prueba de contenido"}]}}', autor=self.user,
                                                  subcategoria=self.subcategoria, estado='PUBLICADO')

    def test_dar_me_gusta(self):
        """
        Prueba de dar "Me gusta" a un contenido estando autenticado.
        Se espera que el "Me gusta" se registre correctamente.
        """
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('dar_me_gusta', args=[self.contenido.id]))
        self.assertEqual(response.status_code, 302)

        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.cantidad_me_gusta, 1)

    def test_dar_me_gusta_anonimo(self):
        """
        Prueba de intento de dar "Me gusta" como usuario anónimo.
        Se espera que el "Me gusta" no se registre.
        """
        # De nuevo, no se llama a self.client.login() porque queremos que el usuario permanezca como anónimo
        response = self.client.post(reverse('dar_me_gusta', args=[self.contenido.id]))

        self.assertEqual(response.status_code,
                         302)  # Asumiendo que redireccionas a una página de inicio de sesión o similar

        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.cantidad_me_gusta, 0)  # El "Me gusta" no debería haber sido registrado

    def test_dar_me_gusta_repetido(self):
        """
        Prueba de dar "Me gusta" a un contenido estando autenticado dos veces consecutivas.
        Se espera que el "Me gusta" solo se cuente una vez.
        """
        self.client.login(username='testuser', password='testpassword')

        # Primer intento de dar "Me gusta"
        response = self.client.post(reverse('dar_me_gusta', args=[self.contenido.id]))
        self.assertEqual(response.status_code, 302)
        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.cantidad_me_gusta, 1)

        # Segundo intento de dar "Me gusta" al mismo contenido
        response = self.client.post(reverse('dar_me_gusta', args=[self.contenido.id]))
        self.assertEqual(response.status_code, 302)
        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.cantidad_me_gusta, 1)


class CompartirContenidoTestCase(TestCase):

    def setUp(self):
        """
        Configuración inicial para los tests de compartir contenido.
        Se crea un usuario, categoría, subcategoría y contenido.
        """
        self.client = Client()
        self.user = Usuario.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.categoria = Categoria.objects.create(nombre="TestCategory", descripcion="This is a test category")
        self.subcategoria = Subcategoria.objects.create(nombre="TestSubcategory", categoria=self.categoria)
        self.contenido = Contenido.objects.create(nombre='Test Contenido', cuerpo='{"html":"<p>Prueba de contenido</p>", "delta": {"ops":[{"insert": "Prueba de contenido"}]}}', autor=self.user,
                                                  subcategoria=self.subcategoria, estado='PUBLICADO')

    def test_compartir_by_authenticated_user(self):
        """
        Prueba de compartir contenido estando autenticado.
        Se espera que el compartir se registre correctamente.
        """
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('compartir_contenido', args=[self.contenido.id]))
        self.assertEqual(response.status_code, 200)  # Asumiendo que la respuesta es un JSON y no una redirección

        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.cantidad_compartir, 1)


    def test_compartir_by_anonymous_user(self):
        """
        Prueba de compartir contenido como usuario anónimo.
        Aunque no es común, este test asume que incluso los usuarios anónimos pueden compartir contenidos.
        """
        response = self.client.post(reverse('compartir_contenido', args=[self.contenido.id]))
        self.assertEqual(response.status_code, 200)

        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.cantidad_compartir, 1)