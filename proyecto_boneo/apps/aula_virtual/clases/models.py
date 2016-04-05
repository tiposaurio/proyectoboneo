from django.db import models

from proyecto_boneo.apps.administracion.planes.models import Materia
from proyecto_boneo.apps.administracion.alumnos.models import Alumno


class ClaseVirtual(models.Model):
    # TODO: Agregar criterios de evaluación y puntaje por ejercicio
    # TODO: Pertenece a un profesor quien la administra o puede ser editada por cualquier profesor
    materia = models.ForeignKey(Materia, related_name='clases_virtuales')
    nombre = models.CharField(max_length=30, default="Clase")
    descripcion = models.CharField(max_length=100)


class EjercicioVirtual(models.Model):
    clase_virtual = models.ForeignKey(ClaseVirtual, related_name='ejercicios')
    orden_prioridad = models.IntegerField(null=True, blank=True)

    def is_ejercicio_virtual_multiple_choice(self):
        return hasattr(self,'ejerciciovirtualmultiplechoice')

    def is_ejercicio_virtual_texto(self):
        return hasattr(self,'ejerciciovirtualtexto')

    def ejercicio_instance(self):
        if (self.is_ejercicio_virtual_multiple_choice()):
            return self.ejerciciovirtualmultiplechoice
        elif(self.is_ejercicio_virtual_texto()):
            return self.ejerciciovirtualtexto
        return


class EjercicioVirtualTexto(EjercicioVirtual):
    ayuda = models.TextField(null=True, blank=True)
    consigna = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.consigna)


class EjercicioVirtualMultipleChoice(EjercicioVirtual):
    ayuda = models.TextField(null=True, blank=True)
    pregunta = models.CharField(max_length=100)
    explicacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.pregunta)


class OpcionEjercicioMultipleChoice(models.Model):
    texto = models.CharField(max_length=100)
    ejercicio = models.ForeignKey(EjercicioVirtualMultipleChoice, related_name='opciones')
    opcion_correcta = models.BooleanField(default=False)


class RespuestaEjercicioVirtual(models.Model):
    alumno = models.ForeignKey(Alumno, related_name='+')
    es_correcta = models.NullBooleanField(null=True,default=None)
    clase_virtual = models.ForeignKey(ClaseVirtual, related_name='+')

    def is_respuesta_virtual_multiple_choice(self):
        return hasattr(self,'respuestaejerciciovirtualmultiplechoice')

    def is_respuesta_virtual_texto(self):
        return hasattr(self,'respuestaejerciciovirtualtexto')

    def respuesta_instance(self):
        if (self.is_respuesta_virtual_multiple_choice()):
            return self.respuestaejerciciovirtualmultiplechoice
        elif(self.is_respuesta_virtual_texto()):
            return self.respuestaejerciciovirtualtexto
        return

class RespuestaEjercicioVirtualTexto(RespuestaEjercicioVirtual):
    texto = models.TextField()
    ejercicio = models.ForeignKey(EjercicioVirtualTexto, related_name='respuestas')


class RespuestaEjercicioVirtualMultipleChoice(RespuestaEjercicioVirtual):
    opcion_seleccionada = models.ForeignKey(OpcionEjercicioMultipleChoice, related_name='+')
    ejercicio = models.ForeignKey(EjercicioVirtualMultipleChoice, related_name='respuestas')
