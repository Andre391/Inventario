from django.forms import ModelForm
from .models import Elemento

class ElementoForm(ModelForm):
    class Meta:
        model = Elemento
        fields = ['nombre','marca','estado','cantidad']