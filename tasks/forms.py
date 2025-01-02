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
        widget=CheckboxSelectMultiple() 
    )


    class Meta:
        model = Asignacion
        fields = ['empleado', 'elementos', 'computador']

    def clean_elementos(self):
        # Aquí puedes manipular los datos de los elementos si es necesario
        elementos = self.cleaned_data.get('elementos')
        # Si necesitas mostrar los elementos como texto en lugar de como objetos,
        # puedes convertirlos en un string.
        if elementos:
            return ', '.join([str(elemento) for elemento in elementos])
        return ''