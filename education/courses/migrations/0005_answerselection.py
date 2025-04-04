# Generated by Django 4.2.16 on 2025-02-16 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_lesson_explanation_question_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_selections', to='courses.question')),
                ('selected_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_answers', to='courses.answer')),
            ],
        ),
    ]
