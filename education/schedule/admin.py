from django.contrib import admin
from django.utils.html import format_html
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'lesson_time', 'lesson_name', 'html_link')

    # Метод для создания ссылки на страницу с расписанием
    def html_link(self, obj):
        # Формируем ссылку для перехода на страницу расписания (можно указать свой URL)
        # В этом примере предполагаем, что страница для каждого дня недели будет доступна
        return format_html('<a href="/schedule/" target="_blank">Перейти к расписанию</a>')

    html_link.short_description = 'Ссылка на расписание'
