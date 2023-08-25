from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Gestor personalizado de usuarios que hereda de BaseUserManager.

    Este gestor proporciona métodos para crear usuarios y superusuarios.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Crea y guarda un usuario con el correo electrónico y la contraseña proporcionados.

        :param email: El correo electrónico del usuario.
        :param password: La contraseña del usuario.
        :param extra_fields: Otros campos adicionales para el usuario.
        :return: El usuario creado.
        """
        if not email:
            raise ValueError('Email obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Crea y guarda un administrador con el correo electrónico y la contraseña proporcionados.

        :param email: El correo electrónico del administrador.
        :param password: La contraseña del administrador.
        :param extra_fields: Otros campos adicionales para el administrador.
        :return: El administrador creado.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        return self.create_user(email, password, **extra_fields)