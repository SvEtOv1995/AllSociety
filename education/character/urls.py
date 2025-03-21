from django.urls import path
from .views import character_status, add_exp, lesson_progress, complete_lesson

urlpatterns = [
    path("status/", character_status, name="character_status"),
    path("add_exp/<int:amount>/", add_exp, name="add_exp"),
    path("lesson_progress/<str:topic>/", lesson_progress, name="lesson_progress"),  # Новый URL для прогресса по урокам
    path("complete_lesson/<int:lesson_id>/", complete_lesson, name="complete_lesson"),  # Новый URL для завершения урока
]