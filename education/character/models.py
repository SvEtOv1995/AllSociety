from django.db import models
from django.contrib.auth.models import User

class CharacterProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)

    def add_experience(self, amount):
        """Добавляет опыт и повышает уровень"""
        self.exp += amount
        if self.exp >= 50:
            self.level += 1
            self.exp = 0
        self.save()

    def get_topic_progress(self):
        """Возвращает прогресс по темам"""
        topics = LessonProgress.objects.filter(user=self.user).values('topic').distinct()
        progress = {}
        for topic in topics:
            completed_lessons = LessonProgress.objects.filter(user=self.user, topic=topic['topic'], completed=True).count()
            progress[topic['topic']] = completed_lessons
        return progress

    def __str__(self):
        return f"{self.user.username} - Уровень: {self.level}, EXP: {self.exp}"

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    lesson_name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.topic} - {self.lesson_name} - {'Завершено' if self.completed else 'Не завершено'}"

class Achievement(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(max_length=50, help_text="Имя иконки из Font Awesome")
    points = models.PositiveIntegerField(default=10, verbose_name="Баллы")
    condition = models.CharField(max_length=100, help_text="Условие получения (например: lessons_completed=5)")

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_achieved = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'achievement')
        verbose_name = "Достижение пользователя"
        verbose_name_plural = "Достижения пользователей"

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"