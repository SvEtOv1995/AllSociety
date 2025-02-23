from django.contrib import admin
from django.utils.html import format_html
from .models import Subject, Topic, Lesson, News, Question, Answer
from .models import Subject, SubjectCalculator, SubjectNotes

# Инлайн для ответов на вопросы
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3  # Количество пустых ответов по умолчанию (можно изменить по желанию)
    fields = ('text', 'is_correct')  # Поля, которые будут отображаться для каждого ответа

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject_image')

    def subject_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;" />', obj.image.url)
        return "Нет изображения"
    subject_image.short_description = "Иконка"

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic_image', 'subject')

    def topic_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="30" height="30" style="border-radius:50%;" />', obj.image.url)
        return "Нет изображения"
    topic_image.short_description = "Иконка"

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_image', 'topic')

    def lesson_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="30" height="30" style="border-radius:50%;" />', obj.image.url)
        return "Нет изображения"
    lesson_image.short_description = "Иконка"

# 📌 Добавляем админку для новостей
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'news_excerpt')
    ordering = ('-published_at',)
    search_fields = ('title', 'content')

    def news_excerpt(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    news_excerpt.short_description = "Содержание"

# 📌 Добавляем админку для вопросов и ответов
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'lesson', 'explanation')
    inlines = [AnswerInline]  # Включаем инлайн для ответов на вопрос

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')

# Не нужно повторно регистрировать модели, если они уже были зарегистрированы.

@admin.register(SubjectCalculator)
class SubjectCalculatorAdmin(admin.ModelAdmin):
    list_display = ("subject", "html_template")
    
# Регистрация модели SubjectNotes с нужными полями для отображения в админке
@admin.register(SubjectNotes)
class SubjectNotesAdmin(admin.ModelAdmin):
    list_display = ('subject', 'notes_content')  # Показываем поле subject и notes_content