# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.IntegerField()),
                ('letra', models.CharField(blank=True, null=True, max_length=1)),
                ('activa', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['anio', 'letra'],
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.IntegerField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='InstanciaCursado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio_cursado', models.IntegerField()),
                ('division', models.ForeignKey(to='planes.Division', related_name='instancias_cursado')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=150)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('anio', models.IntegerField()),
            ],
            options={
                'ordering': ['anio', 'descripcion'],
            },
        ),
        migrations.AddField(
            model_name='instanciacursado',
            name='materia',
            field=models.ForeignKey(to='planes.Materia', related_name='instancias_cursado'),
        ),
        migrations.AddField(
            model_name='instanciacursado',
            name='profesor_titular',
            field=models.ForeignKey(to='personal.Profesor', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='horario',
            name='instancia_cursado',
            field=models.ForeignKey(to='planes.InstanciaCursado', related_name='horarios'),
        ),
    ]
