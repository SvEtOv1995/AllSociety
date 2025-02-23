from django.shortcuts import render, get_object_or_404
from .forms import AlgebraForm, GeometryForm
from .models import AlgebraCalculation, GeometryCalculation
from .models import MathEntry
from django.http import JsonResponse
from courses.models import SubjectCalculator, Subject  # Импорт моделей
from .forms import PhysicsForm
from .models import PhysicsCalculation

# Функция для вычислений в алгебре
import sympy as sp

def evaluate_expression(expression):
    try:
        return float(sp.sympify(expression))
    except:
        return None

def algebra_view(request):
    form = AlgebraForm(request.POST or None)
    result = None
    if form.is_valid():
        expression = form.cleaned_data['expression']
        result = evaluate_expression(expression)
        AlgebraCalculation.objects.create(expression=expression, result=result)
    return render(request, 'algebra.html', {'form': form, 'result': result})

# Функция для геометрических вычислений
def geometry_view(request):
    form = GeometryForm(request.POST or None)
    result = None
    if form.is_valid():
        shape = form.cleaned_data['shape'].lower()
        dimension = form.cleaned_data['dimension']
        if shape == 'circle':
            result = 3.14 * (dimension ** 2)  # Площадь круга
        elif shape == 'square':
            result = dimension ** 2  # Площадь квадрата
        GeometryCalculation.objects.create(shape=shape, dimension=dimension, result=result)
    return render(request, 'geometry.html', {'form': form, 'result': result})

def fizika_view(request):
    form = PhysicsForm(request.POST or None)
    result = None
    if form.is_valid():
        formula = form.cleaned_data['formula'].lower()
        value1 = form.cleaned_data['value1']
        value2 = form.cleaned_data.get('value2', None)

        if formula == 'kinetic_energy' and value2 is not None:
            result = 0.5 * value1 * (value2 ** 2)  # Кинетическая энергия: 0.5 * m * v^2
        elif formula == 'force' and value2 is not None:
            result = value1 * value2  # Сила: F = m * a

        PhysicsCalculation.objects.create(formula=formula, value1=value1, value2=value2, result=result)

    return render(request, 'fizika.html', {'form': form, 'result': result})

def index(request):
    return render(request, 'index.html')

def math_list(request):
    entries = MathEntry.objects.all().order_by('-created_at')
    return render(request, 'math_list.html', {'entries': entries})

def get_entries(request):
    category = request.GET.get('category')
    if category not in ['algebra', 'geometry']:
        return JsonResponse({'error': 'Invalid category'}, status=400)

    entries = MathEntry.objects.filter(category=category).order_by('-created_at')
    data = [{'title': entry.title, 'content': entry.content} for entry in entries]
    
    return JsonResponse(data, safe=False)


def subject_calculator_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    calculator = SubjectCalculator.objects.filter(subject=subject).first()

    return render(request, "index.html", {
        "subject": subject,
        "calculator": calculator
    })
