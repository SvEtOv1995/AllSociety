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