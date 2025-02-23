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

class PhysicsForm(forms.Form):
    FORMULAS = [
        ('kinetic_energy', 'Кинетическая энергия (0.5 * m * v²)'),
        ('force', 'Сила (F = m * a)')
    ]
    formula = forms.ChoiceField(choices=FORMULAS, label="Выберите формулу")
    value1 = forms.FloatField(label="Первое значение (масса или сила)")
    value2 = forms.FloatField(label="Второе значение (скорость или ускорение)", required=False)