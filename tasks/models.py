from django.db import models
from django.contrib.auth.models import  User

# Create your models here.
class Elemento(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.nombre} - de {self.user}'

class Equipo(models.Model):
    serial = models.CharField(max_length=100, primary_key=True) 
    marca = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.serial} - de {self.user}'


class Asignacion(models.Model):
    empleado = models.ForeignKey(User, on_delete=models.CASCADE)  
    elementos = models.ManyToManyField(Elemento) 

    def __str__(self):
        return f'Asignación de {self.empleado.username} a {self.elementos.count()} elementos'