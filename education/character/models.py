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

    def __str__(self):
        return f"{self.user.username} - Уровень: {self.level}, EXP: {self.exp}"
