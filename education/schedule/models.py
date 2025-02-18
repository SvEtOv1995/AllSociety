from django.db import models

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
    ]
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    lesson_time = models.TimeField()
    lesson_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.day_of_week} - {self.lesson_name} ({self.lesson_time})"
