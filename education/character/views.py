from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CharacterProgress, LessonProgress

@login_required
def character_status(request):
    """Страница со статистикой персонажа"""
    progress, created = CharacterProgress.objects.get_or_create(user=request.user)

    # Рассчитываем количество пройденных уроков (10 опыта = 1 урок)
    lessons_completed = progress.exp // 10

    # Рассчитываем оставшийся опыт до следующего уровня
    remaining_exp = 50 - (progress.exp % 50) if progress.exp % 50 != 0 else 0

    # Получаем прогресс по темам
    topic_progress = progress.get_topic_progress()

    return render(request, "status.html", {
        "progress": progress,
        "lessons_completed": lessons_completed,
        "remaining_exp": remaining_exp,
        "topic_progress": topic_progress
    })

@login_required
def add_exp(request, amount):
    """Добавляет опыт персонажу"""
    progress, created = CharacterProgress.objects.get_or_create(user=request.user)
    progress.add_experience(amount)
    return redirect("character_status")

@login_required
def lesson_progress(request, topic):
    """Отображает прогресс по урокам в определенной теме"""
    lessons = LessonProgress.objects.filter(user=request.user, topic=topic)
    return render(request, "lesson_progress.html", {
        "topic": topic,
        "lessons": lessons
    })

@login_required
def complete_lesson(request, lesson_id):
    """Отмечает урок как завершенный и добавляет опыт"""
    lesson = get_object_or_404(LessonProgress, id=lesson_id, user=request.user)
    if not lesson.completed:
        lesson.completed = True
        lesson.save()
        progress, created = CharacterProgress.objects.get_or_create(user=request.user)
        progress.add_experience(10)  # Добавляем 10 опыта за завершенный урок
    return redirect("lesson_progress", topic=lesson.topic)