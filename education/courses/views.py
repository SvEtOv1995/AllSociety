from django.shortcuts import render, get_object_or_404
from .models import Subject, Topic, Lesson, News
from django.shortcuts import redirect
from .models import Question, Answer

def subjects_list(request):
    subjects = Subject.objects.all()
    news = News.objects.order_by('-published_at')[:5]  # Показываем 5 последних новостей
    return render(request, 'subjects_list.html', {'subjects': subjects, 'news': news})

def topic_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    topics = subject.topics.all()
    return render(request, 'topic_list.html', {'subject': subject, 'topics': topics})

def lesson_list(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    lessons = topic.lessons.all()
    return render(request, 'lesson_list.html', {'topic': topic, 'lessons': lessons})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'lesson_detail.html', {'lesson': lesson})

def check_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    correct_answer = question.answers.filter(is_correct=True).first()  # Найдем правильный ответ

    result = ""
    explanation = ""

    if request.method == "POST":
        # Получаем выбранный ответ
        selected_answer_id = request.POST.get('answer')
        selected_answer = get_object_or_404(Answer, id=selected_answer_id)

        # Проверяем правильность ответа
        if selected_answer == correct_answer:
            result = "Правильный ответ!"
            explanation = question.explanation  # Отображаем пояснение
        else:
            result = "Неправильный ответ!"

    # Отправляем результат и объяснение в шаблон
    return render(request, 'lesson_detail.html', {
        'lesson': question.lesson,
        'result': result,
        'explanation': explanation,
    })
