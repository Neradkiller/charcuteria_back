# Generated by Django 3.1.4 on 2020-12-29 01:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True, verbose_name='password')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('is_super', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('A', 'Administrador'), ('C', 'Cliente')], default='C', max_length=1)),
            ],
            options={
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name1', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('lastname1', models.CharField(max_length=100)),
                ('doc_identidad', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'perfil',
            },
        ),
    ]
