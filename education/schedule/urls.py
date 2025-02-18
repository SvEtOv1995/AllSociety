from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_view, name='schedule'),  # Главная страница для отображения расписания
]
