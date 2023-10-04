from django.test import TestCase
from django.urls import reverse

from .models import Plantilla, Contenido
from usuarios.models import Usuario
from roles.models import CustomRole, CustomPermission, RolePermission, UserCategoryRole
from categorias.models import Categoria, Subcategoria
from parametros.models import Parametro


class ContenidoViewsTestCase(TestCase):
    def setUp(self):
        # Crea el rol de Admin
        CustomRole.objects.get_or_create(name='Admin', is_system_role=True)
        self.first_user = Usuario.objects.create_user(username='testadmin',
                                                      email='testadmin@gmail.com',
                                                      password='test1password')

        # Configura el entorno de prueba, como usuarios, plantillas y contenido

        self.user = Usuario.objects.create_user(username='testuser', email='testuser@gmail.com',
                                                password='testpassword')

        # Crea los roles con sus permisos necesarios
        self.permission_autor = CustomPermission(name='create_content', description='Crear Contenido')
        self.permission_autor.save()
        self.permission_editor = CustomPermission(name='edit_content', description='Editar Contenido')
        self.permission_editor.save()
        self.permission_publicador = CustomPermission(name='approve_content', description='Aprobar Contenido')
        self.permission_publicador.save()
        self.permission_report = CustomPermission(name='report_content', description='Reportar contenido')
        self.permission_report.save()

        self.rol_autor = CustomRole.objects.create(name='autor')
        self.rol_editor = CustomRole.objects.create(name='editor')
        self.rol_publicador = CustomRole.objects.create(name='publicador')
        self.rol_report = CustomRole.objects.create(name='report')

        self.categoria = Categoria.objects.create(nombre='Prueba', descripcion='Categoria de Prueba')

        self.plantilla = Plantilla.objects.create(descripcion='Plantilla de prueba',
                                                  plantilla='{"html":"<p>Prueba de plantilla</p>", "delta": {"ops":[{"insert": "Prueba de plantilla"}]}}')

        self.rol_perm_autor = RolePermission.objects.create(role=self.rol_autor, permission=self.permission_autor)
        self.rol_perm_editor = RolePermission.objects.create(role=self.rol_editor, permission=self.permission_editor)
        self.rol_perm_publicador = RolePermission.objects.create(role=self.rol_publicador, permission=self.permission_publicador)
        self.rol_perm_report = RolePermission.objects.create(role=self.rol_report, permission=self.permission_report)

        self.subcategoria = Subcategoria.objects.create(nombre='SubPrueba', categoria=self.categoria)

        # Contenido
        self.contenido = Contenido.objects.create(nombre='Prueba',
                                                  cuerpo='{"html":"<p>Prueba de contenido</p>", "delta": {"ops":[{"insert": "Prueba de contenido"}]}}',
                                                  autor=self.user,
                                                  subcategoria=self.subcategoria,
                                                  estado='BORRADOR')

        # Crea un parámetro de prueba para la cantidad máxima de denuncias
        self.parametro = Parametro.objects.create(clave='MAX_CANT_DENUNCIAS', valor='3')


# Seleccionar Plantilla
    def test_seleccionar_plantilla(self):
        """
        Prueba que la vista seleccionar plantilla se muestre a un usuario con permiso de autor ('create_content')
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_autor)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('seleccionar_plantilla', args=[self.categoria.id]))
        self.assertEqual(response.status_code, 200)

    def test_seleccionar_plantilla_not_logged_in(self):
        """
        Prueba que la vista seleccionar plantilla redirige a un usuario si es que no ha iniciado sesión.
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_autor)
        response = self.client.get(reverse('seleccionar_plantilla', args=[self.categoria.id]))
        self.assertEqual(response.status_code, 302)

    def test_seleccionar_plantilla_no_permission(self):
        """
        Prueba que la vista seleccionar plantilla no se muestre a un usuario si no tiene el permiso necesario.
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('seleccionar_plantilla', args=[self.categoria.id]))
        self.assertEqual(response.status_code, 403)

# Previsualizar plantilla
    def test_previsualizar(self):
        """
        Prueba que la vista previsualizar plantillas se muestra para un usuario
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('previsualizar', args=[self.plantilla.id]))
        self.assertEqual(response.status_code, 200)

    def test_previsualizar_not_logged_in(self):
        """
        Prueba que la vista previsualizar plantilla redirige a un usuario si es que no ha iniciado sesión.
        :return:
        """
        response = self.client.get(reverse('previsualizar', args=[self.plantilla.id]))
        self.assertEqual(response.status_code, 302)


# Crear Contenido
    def test_crear_contenido(self):
        """
        Prueba que la vista crear contenido se muestre a un usuario con permiso de autor ('create_content')
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_autor)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('crear_contenido', args=[self.categoria.id, self.plantilla.id]))
        self.assertEqual(response.status_code, 200)

    def test_crear_contenido_not_logged_in(self):
        """
        Prueba que la vista crear contenido redirige a un usuario si es que no ha iniciado sesión.
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_autor)
        response = self.client.get(reverse('crear_contenido', args=[self.categoria.id, self.plantilla.id]))
        self.assertEqual(response.status_code, 302)

    def test_crear_contenido_no_permission(self):
        """
        Prueba que la vista crear contenido no se muestre a un usuario si no tiene el permiso necesario.
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('crear_contenido', args=[self.categoria.id, self.plantilla.id]))
        self.assertEqual(response.status_code, 403)

# Ver contenido
    def test_ver_contenido(self):
        """
        Prueba que la vista ver contenido se muestre a un usuario registrado
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('ver_contenido', args=[self.contenido.id]))
        self.assertEqual(response.status_code, 200)

    def test_ver_contenido_not_logged_in(self):
        """
        Prueba que la vista ver contenido se muestra a un usuario aunque no haya iniciado sesión.
        :return:
        """
        response = self.client.get(reverse('ver_contenido', args=[self.contenido.id]))
        self.assertEqual(response.status_code, 200)

# Editar Contenido
    def test_editar_contenido_as_autor(self):
        """
        Prueba que la vista editar contenido se muestre a un usuario con permiso de autor ('create_content')
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_autor)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('editar_contenido', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 200)

    def test_editar_contenido_as_editor(self):
        """
        Prueba que la vista editar contenido se muestre a un usuario con permiso de editor ('edit_content')
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_editor)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('editar_contenido', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 200)

    def test_editar_contenido_not_logged_in(self):
        """
        Prueba que la vista editar contenido redirige a un usuario si es que no ha iniciado sesión.
        :return:
        """
        response = self.client.get(reverse('editar_contenido', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 302)

    def test_editar_contenido_no_permission(self):
        """
        Prueba que la vista editar contenido no se muestre a un usuario si no tiene el permiso necesario.
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('editar_contenido', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 403)

# Aprobar Contenido
    def test_aprobar_contenido(self):
        """
        Prueba que la vista aprobar contenido se muestre a un usuario con permiso de publicador ('approve_content')
        :return:
        """
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_publicador)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('aprobar_contenido', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 200)

    def test_aprobar_contenido_not_logged_in(self):
        """
        Prueba que la vista aprobar contenido redirige a un usuario si es que no ha iniciado sesión.
        :return:
        """
        response = self.client.get(reverse('aprobar_contenido', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 302)

    def test_aprobar_contenido_no_permission(self):
        """
        Prueba que la vista aprobar contenido no se muestre a un usuario si no tiene el permiso necesario.
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('aprobar_contenido', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 403)

# Rechazar Contenido
    def test_rechazar_contenido(self):
        """
        Prueba que la vista rechazar contenido redirige correctamente a un usuario con permiso de publicador ('approve_content')
        y pase el estado del contenido a 'Rechazado'.
        :return:
        """
        # Asigna el rol publicador al usuario
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_publicador)

        # Inicia sesión como el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Obtiene la URL de la vista con los parámetros necesarios
        url = reverse('rechazar_contenido', kwargs={'categoria_id': self.categoria.id, 'contenido_id': self.contenido.id})

        # Realiza una solicitud POST a la vista
        response = self.client.post(url)

        # Verifica que la respuesta sea una redirección (código de estado 302)
        self.assertEqual(response.status_code, 302)

        # Actualiza el objeto de contenido desde la base de datos
        self.contenido.refresh_from_db()

        # Verifica que el estado del contenido sea 'RECHAZADO'
        self.assertEqual(self.contenido.estado, 'RECHAZADO')

    def test_rechazar_contenido_not_logged_in(self):
        """
        Prueba que la vista para enviar el contenido a edición redirige a un usuario si es que no ha iniciado sesión.
        :return:
        """
        # Obtiene la URL de la vista con los parámetros necesarios
        url = reverse('rechazar_contenido', kwargs={'categoria_id': self.categoria.id, 'contenido_id': self.contenido.id})

        # Realiza una solicitud POST a la vista sin autenticación
        response = self.client.post(url)

        # Verifica que la respuesta sea una redirección a la página de inicio de sesión
        self.assertRedirects(response, '/?next=' + url)

    def test_rechazar_contenido_no_permission(self):
        """
        Prueba que la vista aprobar contenido no se muestre a un usuario si no tiene el permiso necesario.
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('rechazar_contenido', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 403)

# Enviar a Edición
    def test_enviar_edicion(self):
        """
        Prueba que la vista para enviar el contenido a edición se muestre a un usuario con permiso de autor ('create_content')
        y pase el estado del contenido a 'En Edicion'.
        :return:
        """
        # Asigna el rol publicador al usuario
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_autor)

        # Inicia sesión como el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Obtiene la URL de la vista con los parámetros necesarios
        url = reverse('enviar_edicion', kwargs={'categoria_id': self.categoria.id, 'contenido_id': self.contenido.id})

        # Realiza una solicitud POST a la vista
        response = self.client.post(url)

        # Verifica que la respuesta sea una redirección (código de estado 302)
        self.assertEqual(response.status_code, 302)

        # Actualiza el objeto de contenido desde la base de datos
        self.contenido.refresh_from_db()

        # Verifica que el estado del contenido sea 'EDICION'
        self.assertEqual(self.contenido.estado, 'EDICION')

    def test_enviar_edicion_not_logged_in(self):
        """
        Prueba que la vista para enviar el contenido a edición redirige a un usuario si es que no ha iniciado sesión.
        :return:
        """
        # Obtiene la URL de la vista con los parámetros necesarios
        url = reverse('enviar_edicion', kwargs={'categoria_id': self.categoria.id, 'contenido_id': self.contenido.id})

        # Realiza una solicitud POST a la vista sin autenticación
        response = self.client.post(url)

        # Verifica que la respuesta sea una redirección a la página de inicio de sesión
        self.assertRedirects(response, '/?next=' + url)

    def test_enviar_edicion_no_permission(self):
        """
        Prueba que la vista para enviar el contenido a edición no se muestre a un usuario si no tiene el permiso necesario.
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('enviar_edicion', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 403)

# Enviar a Revisión
    def test_enviar_revision(self):
        """
        Prueba que la vista para enviar el contenido a revisión se muestre a un usuario con permiso de editor ('create_content')
        y pase el estado del contenido a 'En Revision'.
        :return:
        """
        # Asigna el rol publicador al usuario
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_editor)

        # Inicia sesión como el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Obtiene la URL de la vista con los parámetros necesarios
        url = reverse('enviar_revision', kwargs={'categoria_id': self.categoria.id, 'contenido_id': self.contenido.id})

        # Realiza una solicitud POST a la vista
        response = self.client.post(url)

        # Verifica que la respuesta sea una redirección (código de estado 302)
        self.assertEqual(response.status_code, 302)

        # Actualiza el objeto de contenido desde la base de datos
        self.contenido.refresh_from_db()

        # Verifica que el estado del contenido sea 'EDICION'
        self.assertEqual(self.contenido.estado, 'REVISION')

    def test_enviar_revision_not_logged_in(self):
        """
        Prueba que la vista para enviar el contenido a revisión redirige a un usuario si es que no ha iniciado sesión.
        :return:
        """
        # Obtiene la URL de la vista con los parámetros necesarios
        url = reverse('enviar_revision', kwargs={'categoria_id': self.categoria.id, 'contenido_id': self.contenido.id})

        # Realiza una solicitud POST a la vista sin autenticación
        response = self.client.post(url)

        # Verifica que la respuesta sea una redirección a la página de inicio de sesión
        self.assertRedirects(response, '/?next=' + url)

    def test_enviar_revision_no_permission(self):
        """
        Prueba que la vista para enviar el contenido a revisión no se muestre a un usuario si no tiene el permiso necesario.
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('enviar_revision', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 403)

# Denunciar Contenido
    def test_denunciar_contenido(self):
        # Asigna el rol al usuario
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_report)

        # Inicia sesión como el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Obtiene la URL de la vista con el ID del contenido
        url = reverse('denunciar_contenido', kwargs={'contenido_id': self.contenido.id})

        # Realiza una solicitud POST a la vista
        response = self.client.post(url)

        # Verifica que la respuesta sea una redirección (código de estado 302)
        self.assertEqual(response.status_code, 302)

        # Actualiza el objeto de contenido desde la base de datos
        self.contenido.refresh_from_db()

        # Verifica que la cantidad de denuncias haya aumentado en 1
        self.assertEqual(self.contenido.cantidad_denuncias, 1)

    def test_denunciar_contenido_con_max_denuncias(self):
        # Asigna el rol al usuario
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_report)

        # Inicia sesión como el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Establece la cantidad de denuncias máxima permitida
        self.parametro.valor = '1'
        self.parametro.save()

        # Obtiene la URL de la vista con el ID del contenido
        url = reverse('denunciar_contenido', kwargs={'contenido_id': self.contenido.id})

        # Realiza una solicitud POST a la vista
        response = self.client.post(url)

        # Verifica que la respuesta sea una redirección (código de estado 302)
        self.assertEqual(response.status_code, 302)

        # Actualiza el objeto de contenido desde la base de datos
        self.contenido.refresh_from_db()

        # Verifica que el estado del contenido sea 'INACTIVO' debido a que alcanzó el máximo de denuncias
        self.assertEqual(self.contenido.estado, 'INACTIVO')

# Inactivar Contenido
    def test_inactivar_contenido(self):
        """
        Prueba que la vista para inactivar el contenido se muestre a un usuario con permiso ('inactivate_content')
        y pase el estado del contenido a 'Inactivo'.
        :return:
        """
        # Crea un rol con permiso para inactivar contenidos
        self.permission_inactivate = CustomPermission(name='inactivate_content', description='Inactivar contenido')
        self.permission_inactivate.save()
        self.rol_inactivate = CustomRole.objects.create(name='inactivate')
        self.rol_perm_inactivate = RolePermission.objects.create(role=self.rol_inactivate, permission=self.permission_inactivate)

        # Asigna el rol al usuario
        self.user_role = UserCategoryRole.objects.create(user=self.user, category=self.categoria, role=self.rol_inactivate)

        # Inicia sesión como el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Obtiene la URL de la vista con los parámetros necesarios
        url = reverse('inactivar_contenido', kwargs={'categoria_id': self.categoria.id, 'contenido_id': self.contenido.id})

        # Realiza una solicitud POST a la vista
        response = self.client.post(url)

        # Verifica que la respuesta sea una redirección (código de estado 302)
        self.assertEqual(response.status_code, 302)

        # Actualiza el objeto de contenido desde la base de datos
        self.contenido.refresh_from_db()

        # Verifica que el estado del contenido sea 'INACTIVO'
        self.assertEqual(self.contenido.estado, 'INACTIVO')

    def test_inactivar_contenido_not_logged_in(self):
        """
        Prueba que la vista para inactivar un contenido redirige a un usuario si es que no ha iniciado sesión.
        :return:
        """
        # Obtiene la URL de la vista con los parámetros necesarios
        url = reverse('inactivar_contenido', kwargs={'categoria_id': self.categoria.id, 'contenido_id': self.contenido.id})

        # Realiza una solicitud POST a la vista sin autenticación
        response = self.client.post(url)

        # Verifica que la respuesta sea una redirección a la página de inicio de sesión
        self.assertRedirects(response, '/?next=' + url)

    def test_inactivar_contenido_no_permission(self):
        """
        Prueba que la vista para inactivar un contenido no se muestre a un usuario si no tiene el permiso necesario.
        :return:
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('inactivar_contenido', args=[self.categoria.id, self.contenido.id]))
        self.assertEqual(response.status_code, 403)
