from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CharacterProgress, LessonProgress, Achievement, UserAchievement

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

@login_required
def achievements_list(request):
    # Все возможные достижения
    all_achievements = Achievement.objects.all()
    
    # Достижения текущего пользователя
    user_achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement')
    
    # Создаем список всех достижений с отметкой о получении
    achievements = []
    for achievement in all_achievements:
        achieved = user_achievements.filter(achievement=achievement).exists()
        achievements.append({
            'achievement': achievement,
            'achieved': achieved,
            'date_achieved': user_achievements.filter(achievement=achievement).first().date_achieved if achieved else None
        })
    
    # Помечаем новые достижения как просмотренные
    UserAchievement.objects.filter(user=request.user, is_seen=False).update(is_seen=True)
    
    return render(request, 'list.html', {
        'achievements': achievements,
        'total_points': sum(ua.achievement.points for ua in user_achievements)
    })

@login_required
def achievement_detail(request, achievement_id):
    achievement = get_object_or_404(Achievement, id=achievement_id)
    user_has = UserAchievement.objects.filter(
        user=request.user, 
        achievement=achievement
    ).exists()
    
    return render(request, 'detail.html', {
        'achievement': achievement,
        'user_has': user_has
    })