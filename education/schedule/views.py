from django.shortcuts import render, redirect
from .models import Schedule
from .forms import ScheduleForm

def schedule_view(request):
    # Словарь с расписанием для каждого дня недели
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    schedule_data = {day: Schedule.objects.filter(day_of_week=day) for day in days_of_week}

    if request.method == 'POST':
        # Обработка изменений расписания
        for day in days_of_week:
            for index, lesson_time in enumerate(request.POST.getlist(f'{day}_time')):
                lesson_name = request.POST.getlist(f'{day}_lesson')[index]
                if lesson_name:
                    schedule_item, created = Schedule.objects.update_or_create(
                        day_of_week=day, lesson_time=lesson_time,
                        defaults={'lesson_name': lesson_name}
                    )
        return redirect('schedule')  # Перенаправление после успешного обновления

    return render(request, 'schedule.html', {'schedule_data': schedule_data})
