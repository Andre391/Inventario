from django.contrib import admin
from .models import Elemento, Equipo, Asignacion, Empleado
# Register your models here.

admin.site.register(Elemento)

admin.site.register(Equipo)

admin.site.register(Asignacion)

admin.site.register(Empleado)
