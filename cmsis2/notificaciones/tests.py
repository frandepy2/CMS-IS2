from django.test import TestCase
from django.urls import reverse

from .utils import crear_notificacion
from .models import Notificacion
from usuarios.models import Usuario
from contenidos.models import Contenido, Subcategoria
from categorias.models import Categoria
# Create your tests here.
class TestCrearNotificacion(TestCase):

    def setUp(self):
        self.first_user = Usuario.objects.create_user(username='user_1', email='usuario1@gmail.com', password='password')
        self.first_user.save()
        self.second_user = Usuario.objects.create_user(username='user_2', email='usuario2@gmail.com', password='password')
        self.second_user.save()
        self.categoria = Categoria.objects.create(nombre='Prueba', descripcion='Categoria de Prueba')
        self.categoria.save()
        self.subcategoria = Subcategoria.objects.create(nombre='SubPrueba', categoria=self.categoria)
        self.subcategoria.save()

        self.contenido = Contenido.objects.create(nombre='Prueba',
                                                  cuerpo='{"html":"<p>Prueba de contenido</p>", "delta": {"ops":[{"insert": "Prueba de contenido"}]}}',
                                                  autor=self.first_user,
                                                  subcategoria=self.subcategoria,
                                                  estado='PUBLICADO')
        self.contenido.save()

    def test_creacion_notificacion(self):
        """
        Test Prueba la creacion correcta de una notificacion
        """
        # Datos de prueba
        emisor = self.first_user
        receptor = self.second_user
        accion = None
        contenido = self.contenido
        titulo = "titulo_prueba"
        mensaje = "mensaje_prueba"
        leido = False

        # Llama a la función
        notificacion = crear_notificacion(
            emisor=emisor,
            receptor=receptor,
            accion=accion,
            contenido=contenido,
            titulo=titulo,
            mensaje=mensaje,
            leido=leido
        )

        # Verifica si la notificación se creó correctamente
        self.assertIsInstance(notificacion, Notificacion)
        self.assertEqual(notificacion.emisor, emisor)
        self.assertEqual(notificacion.receptor, receptor)
        self.assertEqual(notificacion.accion, accion)
        self.assertEqual(notificacion.contenido, contenido)
        self.assertEqual(notificacion.titulo, titulo)
        self.assertEqual(notificacion.mensaje, mensaje)
        self.assertEqual(notificacion.leido, leido)

    def test_leer_notificacion(self):
        """
        Test que prueba que se marque como leido una notificacion
        """
        # Datos de prueba
        emisor = self.first_user
        receptor = self.second_user
        accion = None
        contenido = self.contenido
        titulo = "titulo_prueba"
        mensaje = "mensaje_prueba"
        leido = False

        notificacion = Notificacion(
            emisor=emisor,
            receptor=receptor,
            accion=accion,
            contenido=contenido,
            titulo=titulo,
            mensaje=mensaje,
            leido=leido
        )
        notificacion.save()

        # Inicia sesión como el usuario
        self.client.login(username='user_2', password='password')

        # Hace la solicitud para marcar la notificación como leída
        response = self.client.get(reverse('leer_notificacion', kwargs={'notificacion_id': notificacion.id}))

        self.assertEqual(response.status_code, 302)

        notificacion_actualizada = Notificacion.objects.get(id=notificacion.id)
        self.assertTrue(notificacion_actualizada.leido)

        self.assertRedirects(response, reverse('ver_contenido', kwargs={'contenido_id': self.contenido.id}))
