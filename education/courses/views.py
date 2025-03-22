from django.shortcuts import render, get_object_or_404
from .models import Subject, Topic, Lesson, News
from django.shortcuts import redirect
from .models import Question, Answer
from .models import Subject, SubjectCalculator, SubjectNotes
from django.utils.safestring import mark_safe
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

def structure_lesson_content(content):
    """
    Функция принимает текст из админ-панели и добавляет классы для стилизации контента.
    - Форматы: заголовки, списки, формулы, абзацы.
    """
    
    # Добавление классов к заголовкам (например, ## Заголовок -> <h2>)
    content = re.sub(r'## (.+)', r'<h2 class="lesson-heading">\1</h2>', content)
    content = re.sub(r'# (.+)', r'<h1 class="lesson-title">\1</h1>', content)

    # Форматирование списков (начинающихся с "- " или "1. ")
    content = re.sub(r'\n- (.+)', r'<li>\1</li>', content)
    content = re.sub(r'\n1\. (.+)', r'<li>\1</li>', content)
    content = re.sub(r'(<li>.+</li>)', r'<ul class="lesson-list">\1</ul>', content)

    # Форматирование формул LaTeX (блоковые и встроенные)
    content = re.sub(r'\$\$(.+?)\$\$', r'<div class="math">\1</div>', content)  # Блоковые формулы
    content = re.sub(r'\$(.+?)\$', r'<span class="math-inline">\1</span>', content)  # Встроенные формулы

    # Добавление классов к абзацам
    content = re.sub(r'\n(.+)', r'<p class="lesson-text">\1</p>', content)

    return mark_safe(content)  # Django считает HTML-безопасным

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Применяем структурирование данных к содержимому урока
    structured_content = structure_lesson_content(lesson.content)
    
    return render(request, 'lesson_detail.html', {'lesson': lesson, 'structured_content': structured_content})


def check_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    correct_answer = question.answers.filter(is_correct=True).first()

    if "answered_questions" not in request.session:
        request.session["answered_questions"] = {}

    result = ""
    explanation = ""

    if request.method == "POST":
        selected_answer_id = request.POST.get("answer")
        selected_answer = get_object_or_404(Answer, id=selected_answer_id)

        if selected_answer == correct_answer:
            result = "Правильный ответ!"
            explanation = question.explanation if question.explanation else "Нет объяснения."
        else:
            result = "Неправильный ответ!"
            explanation = "Попробуйте еще раз."

        # Сохраняем ответ в сессии с корректной структурой
        request.session["answered_questions"][str(question_id)] = {
            "selected_answer": str(selected_answer_id),  # Приводим ID к строке
            "result": result,  # Добавляем результат
            "explanation": explanation,  # Добавляем объяснение
        }
        request.session.modified = True

    return render(request, "lesson_detail.html", {
        "lesson": question.lesson,
        "answered_questions": request.session["answered_questions"],  # Отправляем в шаблон
    })


def subject_calculator(request, subject_id):
    # Get the subject object
    subject = get_object_or_404(Subject, id=subject_id)
    
    # Try to get the corresponding SubjectCalculator instance
    try:
        calculator = SubjectCalculator.objects.get(subject=subject)
    except SubjectCalculator.DoesNotExist:
        calculator = None  # Or handle the case when the calculator doesn't exist
    
    return render(request, 'subject_calculator.html', {'subject': subject, 'calculator': calculator})

# View for Subject's Notes
def subject_notes(request, subject_id):
    # Get the subject object
    subject = get_object_or_404(Subject, id=subject_id)
    
    # Try to get the corresponding SubjectNotes instance
    try:
        notes = SubjectNotes.objects.get(subject=subject)
    except SubjectNotes.DoesNotExist:
        notes = None  # Or handle the case when the notes don't exist
    
    return render(request, 'subject_notes.html', {'subject': subject, 'notes': notes})

@csrf_exempt
def save_board_data(request, lesson_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            board_data = data.get('board_data')
            lesson = Lesson.objects.get(id=lesson_id)
            lesson.board_data = board_data
            lesson.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Функция для получения данных доски
def get_board_data(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        return JsonResponse({'board_data': lesson.board_data})
    except Lesson.DoesNotExist:
        return JsonResponse({'error': 'Lesson not found'}, status=404)

# Функция для сохранения данных доски
@csrf_exempt
def save_board_data(request, lesson_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            board_data = data.get('board_data')
            lesson = Lesson.objects.get(id=lesson_id)
            lesson.board_data = board_data
            lesson.save()
            return JsonResponse({'success': True})
        except Lesson.DoesNotExist:
            return JsonResponse({'error': 'Lesson not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)