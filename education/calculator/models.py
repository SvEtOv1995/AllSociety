from django.db import models
from django.utils.html import format_html

class AlgebraCalculation(models.Model):
    expression = models.CharField(max_length=255)
    result = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.expression} = {self.result}"

class GeometryCalculation(models.Model):
    shape = models.CharField(max_length=100)
    dimension = models.FloatField()
    result = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.shape} ({self.dimension}) = {self.result}"

class MathEntry(models.Model):
    CATEGORY_CHOICES = [
        ('algebra', 'Алгебра'),
        ('geometry', 'Геометрия'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="LaTeX-код")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"