import csv
import datetime
import os
import random

from django.core.management import BaseCommand

from proyecto_boneo.apps.administracion.alumnos.models import Alumno, Responsable, InscripcionAlumno
from proyecto_boneo.apps.administracion.personal.models import Profesor
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo
from proyecto_boneo.apps.administracion.planes.models import Division, InstanciaCursado, Materia

BASE_DIR = os.path.dirname(__file__)


class Command(BaseCommand):
    help = 'This command populates the database with initial data'

    años_plan = range(1, 6)
    cantidad_divisiones = 4

    models = [
        Alumno,
        InscripcionAlumno,
        InstanciaCursado,
        Materia,
        Profesor,
        Responsable,
        UsuarioBoneo
    ]

    def _get_random_person_data(self):
        nombre = random.choice(self.names)
        apellido = random.choice(self.last_names)
        return {
            'nombre': nombre,
            'apellido': apellido,
            'dni': random.randint(2*10**7, 4*10**7),
            'domicilio': '{} {}'.format(random.choice(self.street_names),
                                        random.randint(100, 3000)),
            'fecha_nacimiento': datetime.date.today() - datetime.timedelta(
                days=random.randint(10, 20) * 360),
            'email': '{}_{}@boneo.com'.format(nombre.lower(), apellido.lower())
        }

    def _bulk_create(self, klass, attributes_list):
        for instance in attributes_list:
            klass.objects.create(**instance)

    def _clean_current_state(self):
        for klass in self.models:
            klass.objects.all().delete()

    def _create_materias(self):
        materias = ['Lengua', 'Matemática', 'Ciencias Sociales', 'Formación Ética y Ciudadana',
                    'Ciencias Naturales', 'Educación Física', 'Música']
        attributes_list = []
        for materia in materias:
            for año in self.años_plan:
                attributes_list.append({'descripcion': materia, 'anio': año})
        self._bulk_create(Materia, attributes_list)

    def _create_divisiones(self):
        for año in self.años_plan:
            Division.objects.configurar_divisiones_año(año, self.cantidad_divisiones)

    def _create_instancias_cursado(self):
        InstanciaCursado.objects.generar_año_actual()

    def _create_responsable(self):
        responsable_data = self._get_random_person_data()
        email = responsable_data.pop('email')
        responsable = Responsable(**responsable_data)
        responsable.crear_usuario(email)
        responsable.save()
        return responsable

    def _create_alumnos(self):
        divisiones = list(Division.objects.all())
        for i in range(0, 1500):
            alumno_data = self._get_random_person_data()
            alumno_data['responsable'] = self._create_responsable()
            alumno_data['division'] = random.choice(divisiones)
            email = alumno_data.pop('email')
            alumno = Alumno(**alumno_data)
            alumno.crear_usuario(email)
            alumno.save()

    def _create_profesores(self):
        for i in range(0, 25):
            profesor_data = self._get_random_person_data()
            email = profesor_data.pop('email')
            profesor = Profesor(**profesor_data)
            profesor.crear_usuario(email)
            profesor.save()

    def _assign_profesores_materias(self):
        profesores = Profesor.objects.all()
        for instancia_cursado in InstanciaCursado.objects.all():
            instancia_cursado.profesor_titular = random.choice(profesores)
            instancia_cursado.save()

    def _create_inscripciones(self):
        for alumno in Alumno.objects.all():
            for instancia_cursado in alumno.division.instancias_cursado.all():
                InscripcionAlumno.objects.create(alumno=alumno,
                                                 instancia_cursado=instancia_cursado)

    def _create_test_users(self):
        UsuarioBoneo.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        alumno = Alumno(nombre='Juan', apellido='Pruebas', dni=36538548,
                        fecha_nacimiento=datetime.datetime.today() - datetime.timedelta(days=365*15),
                        responsable=self._create_responsable())
        alumno.crear_usuario('alumno@alumno.com')
        alumno.save()
        profesor = Profesor(nombre='Alberto', apellido='Pruebas',
                            dni=26538548,
                            fecha_nacimiento=datetime.datetime.today() - datetime.timedelta(days=365*33))
        profesor.crear_usuario('profesor@profesor.com')
        profesor.save()

    def _load_data(self):
        self.names = []
        self.last_names = []

        with open(os.path.join(BASE_DIR, 'data/first_names.csv')) as names_file:
            names = csv.reader(names_file)
            for name in names:
                self.names.append(name[0])

        with open(os.path.join(BASE_DIR, 'data/last_names.csv')) as last_names_file:
            last_names = csv.reader(last_names_file)
            for last_name in last_names:
                self.last_names.append(last_name[0])

        self.street_names = []
        with open(os.path.join(BASE_DIR, 'data/street_names.csv')) as street_names:
            street_names = csv.reader(street_names)
            for street_name in street_names:
                self.street_names.append(street_name[0])

    def handle(self, *args, **options):
        self.stdout.write('Cargando información inicial...')
        self._load_data()
        self.stdout.write('Limpiando estado actual...')
        self._clean_current_state()
        self.stdout.write('Creando usuarios de pruebas...')
        self._create_test_users()
        self.stdout.write('Creando materias...')
        self._create_materias()
        self.stdout.write('Creando divisiones...')
        self._create_divisiones()
        self.stdout.write('Creando instancias de cursado...')
        self._create_instancias_cursado()
        self.stdout.write('Creando profesores...')
        self._create_profesores()
        self.stdout.write('Creando alumnos...')
        self._create_alumnos()
        self.stdout.write('Asignando profesores a materias...')
        self._assign_profesores_materias()
        self.stdout.write('Creando inscripciones...')
        self._create_inscripciones()
        self.stdout.write('Listo :)')
