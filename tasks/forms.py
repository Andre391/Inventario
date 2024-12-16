from django.forms import ModelForm
from .models import Elemento, Equipo, Empleado

class ElementoForm(ModelForm):
    class Meta:
        model = Elemento
        fields = ['nombre','marca','estado','cantidad']
        
class EquipoForm(ModelForm):
    class Meta:
        model = Equipo
        fields = ['serial','marca','ubicacion','estado','tipo']
        
class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = ['codigo','nombre','cargo'] 