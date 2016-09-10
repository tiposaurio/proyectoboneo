# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('dni', models.BigIntegerField()),
                ('domicilio', models.CharField(max_length=150)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('fecha_nacimiento', models.DateField()),
                ('legajo', models.BigIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha', models.DateField()),
                ('asistio', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='InscripcionAlumno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='Responsable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('dni', models.BigIntegerField()),
                ('domicilio', models.CharField(max_length=150)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('fecha_nacimiento', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
