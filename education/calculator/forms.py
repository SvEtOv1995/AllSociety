from django import forms
from .models import AlgebraCalculation, GeometryCalculation

class AlgebraForm(forms.ModelForm):
    class Meta:
        model = AlgebraCalculation
        fields = ['expression']

class GeometryForm(forms.ModelForm):
    class Meta:
        model = GeometryCalculation
        fields = ['shape', 'dimension']