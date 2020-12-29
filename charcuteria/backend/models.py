from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Usuario debe tener email")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusuarios deben tener contraseña.')

        user = self.create_user(email, password)
        user.is_super = True
        user.is_staff = True
        user.is_admin = True
        user.role = 'A'
        user.save()

        return user


class User(AbstractBaseUser):

    ROLE_CHOICES =[
        ('A','Administrador'),
        ('C','Cliente'),
    ]

    email = models.CharField(max_length=100, blank=False, null=False, unique=True)
    password = models.CharField(max_length=128, null=True, blank=True, verbose_name='password')
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)   
    is_super = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='C')
    
    def has_perm(self, perm, obj=None):
        return self.is_super

    def has_module_perms(self, app_label):
        return self.is_super
    
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'cliente'

class Direccion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direccion')
    direccion = models.CharField(max_length=400, blank=False, null=False)

    class Meta:
        db_table = 'direccion'

class Perfil(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    name = models.CharField(max_length=100, blank=False, null=False)
    name1 = models.CharField(max_length=100, blank=False, null=False)
    lastname = models.CharField(max_length=100, blank=False, null=False)
    lastname1 = models.CharField(max_length=100, blank=False, null=False)
    doc_identidad = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = 'perfil'