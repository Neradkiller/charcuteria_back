from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None):
        if not email:
            raise ValueError("Usuario debe tener email")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_super = False
        user.is_staff = False
        user.is_admin = False
        user.role = role
        user.save(using=self.db)
        return user


    def create_superuser(self, email, password=None):

        if not email:
            raise ValueError("Usuario debe tener email")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_super = True
        user.is_staff = True
        user.is_admin = True
        user.role = 'A'
        user.save(using=self.db)
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
    is_super = models.BooleanField(null=True, blank=True,)
    is_staff = models.BooleanField(null=True, blank=True,)
    is_admin = models.BooleanField(null=True, blank=True,)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES,)
    
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

class Producto(models.Model):
    
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=5, blank=False, null=False, unique=True)
    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.CharField(max_length=300, blank=False, null=False)
    marca = models.CharField(max_length=50, blank=False, null=False)
    tipo = models.CharField(max_length=50, blank=False, null=False)
    fecha_vencimiento = models.DateField(blank=False, null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0)
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = 'producto'

