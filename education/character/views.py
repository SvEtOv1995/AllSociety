from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CharacterProgress

@login_required
def character_status(request):
    """Страница со статистикой персонажа"""
    progress, created = CharacterProgress.objects.get_or_create(user=request.user)

    # Рассчитываем количество пройденных уроков (10 опыта = 1 урок)
    lessons_completed = progress.exp // 10

    # Рассчитываем оставшийся опыт до следующего уровня
    remaining_exp = 50 - (progress.exp % 50) if progress.exp % 50 != 0 else 0

    return render(request, "status.html", {
        "progress": progress,
        "lessons_completed": lessons_completed,
        "remaining_exp": remaining_exp
    })


@login_required
def add_exp(request, amount):
    """Добавляет опыт персонажу"""
    progress, created = CharacterProgress.objects.get_or_create(user=request.user)
    progress.add_experience(amount)
    return redirect("character_status")
