# Generated by Django 5.2 on 2025-05-12 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='subject',
            field=models.CharField(choices=[('Информатика', 1), ('Математика профильная', 2), ('Математика базовая', 3), ('Математика', 4), ('Физика', 5), ('Русский язык', 6), ('Английский язык', 7), ('Литература', 8), ('Биология', 9), ('Химия', 10), ('История', 11), ('Обществознание', 12)], default='Информатика', verbose_name='Название предмета'),
        ),
    ]
