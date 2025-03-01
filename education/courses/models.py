from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название предмета")
    image = models.ImageField(upload_to='subjects/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        ordering = ['name']
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics', verbose_name="Предмет")
    name = models.CharField(max_length=255, verbose_name="Название темы")
    image = models.ImageField(upload_to='topics/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        ordering = ['subject', 'name']
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self):
        return f"{self.subject.name} - {self.name}"


class Lesson(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='lessons', verbose_name="Тема")
    title = models.CharField(max_length=255, verbose_name="Название урока")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to='lessons/', blank=True, null=True, verbose_name="Изображение")
    allow_latex = models.BooleanField(default=True, verbose_name="Разрешить LaTeX")
    explanation = models.TextField(blank=True, null=True, verbose_name="Объяснение урока")
    svg_content = models.TextField(blank=True, null=True, verbose_name="SVG-код")

    class Meta:
        ordering = ['topic', 'title']
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.topic.name} - {self.title}"


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='questions', on_delete=models.CASCADE, verbose_name="Урок")
    question_text = models.TextField(verbose_name="Текст вопроса")
    explanation = models.TextField(blank=True, null=True, verbose_name="Объяснение ответа")

    class Meta:
        ordering = ['lesson']
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"Вопрос: {self.question_text[:50]}..."


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.CharField(max_length=255, verbose_name="Вариант ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    class Meta:
        ordering = ['question']
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"Ответ: {self.text} ({'✔' if self.is_correct else '✘'})"

    def check_answer(self, selected_answer_id):
        return selected_answer_id == self.id


class AnswerSelection(models.Model):
    question = models.ForeignKey(Question, related_name='answer_selections', on_delete=models.CASCADE, verbose_name="Вопрос")
    selected_answer = models.ForeignKey(Answer, related_name='selected_answers', on_delete=models.CASCADE, verbose_name="Выбранный ответ")

    class Meta:
        ordering = ['question']
        verbose_name = "Выбранный ответ"
        verbose_name_plural = "Выбранные ответы"

    def __str__(self):
        return f"Выбор ответа для: {self.question.question_text[:50]}..."

    def is_answer_correct(self):
        return self.selected_answer.is_correct


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name="Изображение")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


class SubjectCalculator(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    html_template = models.CharField(max_length=255, help_text="Путь к HTML-шаблону или URL", verbose_name="HTML-шаблон")

    class Meta:
        verbose_name = "Калькулятор"
        verbose_name_plural = "Калькуляторы"

    def __str__(self):
        return f"Калькулятор для {self.subject.name}"


class SubjectNotes(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    notes_content = models.TextField(blank=True, null=True, verbose_name="Конспект")

    class Meta:
        verbose_name = "Конспект"
        verbose_name_plural = "Конспекты"

    def __str__(self):
        return f"Конспект для {self.subject.name}"
