from django.shortcuts import render, get_object_or_404
from .models import Subject, Topic, Lesson, News
from django.shortcuts import redirect
from .models import Question, Answer
from .models import Subject, SubjectCalculator, SubjectNotes

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

from django.shortcuts import get_object_or_404, render
from .models import Question, Answer

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