# Generated by Django 5.2 on 2025-05-11 14:14

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название предмета')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('correct_answer', models.CharField(blank=True, max_length=255)),
                ('is_auto', models.BooleanField(default=True)),
                ('ball', models.IntegerField(default=1)),
                ('exam_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='user_photos/')),
                ('is_teacher', models.BooleanField(default=False, verbose_name='Учитель ли')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Администратор ли')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название курса')),
                ('content', models.TextField(blank=True, verbose_name='Описание курса')),
                ('month', models.CharField(choices=[('Январь', 1), ('Февраль', 2), ('Март', 3), ('Апрель', 4), ('Май', 5), ('Июнь', 6), ('Июль', 7), ('Август', 8), ('Сентябрь', 9), ('Октябрь', 10), ('Ноябрь', 11), ('Декабрь', 12)], default='Январь', verbose_name='Месяц')),
                ('subject', models.CharField(choices=[('Информатика', 1), ('Математика профильная', 2), ('Математика базовая', 3), ('Математика', 4), ('Физика', 5), ('Русский язык', 6), ('Английский язык', 7), ('Литература', 8), ('Биология', 9), ('Химия', 10), ('История', 11), ('Обществознание', 12)], default='Информатика', verbose_name='Название предмета')),
                ('students', models.ManyToManyField(blank=True, related_name='courses', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Учитель курса')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True, verbose_name='Описание урока')),
                ('lesson_date', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='learn_api.course')),
            ],
        ),
        migrations.CreateModel(
            name='LessonFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='lesson_files/')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='learn_api.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('lesson', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='homework', to='learn_api.lesson')),
                ('tasks', models.ManyToManyField(to='learn_api.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='task_files/')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='learn_api.task')),
            ],
        ),
        migrations.CreateModel(
            name='UserHomeworkResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('result', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True)),
                ('homework', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='learn_api.homework')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserTaskAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('answers_text', models.CharField(blank=True, max_length=1023)),
                ('correct_answer', models.CharField(blank=True, max_length=1023)),
                ('is_auto', models.BooleanField(default=True)),
                ('result', models.IntegerField(default=0)),
                ('homework_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_results', to='learn_api.userhomeworkresult')),
            ],
        ),
        migrations.CreateModel(
            name='UserTaskAnswerFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='usertaskanswer_files/')),
                ('usertaskanswer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='learn_api.usertaskanswer')),
            ],
        ),
    ]
