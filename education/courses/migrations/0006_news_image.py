# Generated by Django 4.2.16 on 2025-02-17 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_answerselection'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='news_images/'),
        ),
    ]
