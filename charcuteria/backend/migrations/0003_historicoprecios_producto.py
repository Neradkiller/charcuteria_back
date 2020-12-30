# Generated by Django 3.1.4 on 2020-12-29 02:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_direccion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=5, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=300)),
                ('marca', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=50)),
                ('fecha_vencimiento', models.DateField()),
            ],
            options={
                'db_table': 'producto',
            },
        ),
        migrations.CreateModel(
            name='HistoricoPrecios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(default=django.utils.timezone.now)),
                ('precio', models.IntegerField()),
                ('fecha_fin', models.DateField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto', to='backend.producto')),
            ],
            options={
                'db_table': 'historico_precio',
            },
        ),
    ]
