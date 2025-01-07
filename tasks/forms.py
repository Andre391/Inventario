from django.forms import ModelForm, ModelMultipleChoiceField, ModelChoiceField, Select, SelectMultiple, CheckboxSelectMultiple
from .models import Elemento, Equipo, Empleado, Asignacion

class ElementoForm(ModelForm):
    class Meta:
        model = Elemento
        fields = ['nombre','marca','estado','cantidad']
        
class EquipoForm(ModelForm):
    class Meta:
        model = Equipo
        fields = ['serial','marca','ubicacion','estado','tipo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalización de los widgets si es necesario
        self.fields['serial'].widget.attrs.update({'class': 'form-control'})
        self.fields['marca'].widget.attrs.update({'class': 'form-control'})
        
class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = ['codigo','nombre','cargo'] 

class AsignacionForm(ModelForm):
    empleado = ModelChoiceField(
        queryset=Empleado.objects.all(),
        empty_label="Seleccione un empleado",
        label="Empleado",
        widget=Select(attrs={'class': 'form-control'})
    )
    
    elementos = ModelMultipleChoiceField(
        queryset=Elemento.objects.all(),
        widget= SelectMultiple(attrs={'class': 'form-select form-select-lg elementos_class'}),
        required=False
    )

    class Meta:
        model = Asignacion
        fields = ['empleado', 'elementos', 'computador']