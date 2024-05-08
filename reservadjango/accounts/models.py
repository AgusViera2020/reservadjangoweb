from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save

class CustomUserManager(BaseUserManager):
    def _create_user(self, nombre, apellido, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con la dirección de correo electrónico y contraseña dadas.
        """
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(nombre=nombre, apellido=apellido, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, nombre, apellido, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nombre, apellido, email, password, **extra_fields)

    def create_superuser(self, nombre, apellido, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') and extra_fields.get('is_superuser'):
            return self._create_user(nombre, apellido, email, password, **extra_fields)
        else:
            raise ValueError('El superusuario debe tener is_staff=True y is_superuser=True.')

class CustomUser(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=15, validators=[MinLengthValidator(7)])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre','apellido','telefono']

    def __str__(self):
        return self.email
    

class Profile (models.Model):
    user  = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    pais = models.TextField(blank=True, null=True)
    ciudad = models.TextField(blank=True, null=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.user)
    

def create_profile (sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

#automate creation of profile
post_save.connect(create_profile, sender=CustomUser)

