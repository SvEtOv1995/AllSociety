from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='subjects/', blank=True, null=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='topics/', blank=True, null=True)

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class Lesson(models.Model):
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='lessons/', blank=True, null=True)
    allow_latex = models.BooleanField(default=True)  # Флаг для включения LaTeX
    explanation = models.TextField(null=True, blank=True)  # Объяснение урока

    def __str__(self):
        return f"{self.topic.name} - {self.title}"

# Модели для задач и вариантов ответов
class Question(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()  # Текст задачи (вопроса)
    explanation = models.TextField(null=True, blank=True)  # Пояснение, которое показывается после ответа

    def __str__(self):
        return f"Question for {self.lesson.title}"

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)  # Текст варианта ответа
    is_correct = models.BooleanField(default=False)  # Правильный ли ответ?

    def __str__(self):
        return f"Answer for {self.question.question_text}"

    # Это метод для проверки, правильный ли ответ
    def check_answer(self, selected_answer_id):
        return selected_answer_id == self.id


# Дополнительная модель для ввода правильного ответа
class AnswerSelection(models.Model):
    question = models.ForeignKey(Question, related_name='answer_selections', on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, related_name='selected_answers', on_delete=models.CASCADE)

    def is_answer_correct(self):
        return self.selected_answer.is_correct

    def __str__(self):
        return f"Answer selection for {self.question.question_text}"

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
