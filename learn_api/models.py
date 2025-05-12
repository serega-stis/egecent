from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    date_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    is_teacher = models.BooleanField(default=False, verbose_name='Учитель ли')
    is_admin = models.BooleanField(default=False, verbose_name='Администратор ли')
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_birth', 'is_teacher', 'is_admin', 'photo']

class Subjects(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название предмета')

    def __str__(self):
        return self.name

class Course(models.Model):
    MONTH_CHOICES = [
        ('Январь', 1), ('Февраль', 2), ('Март', 3), ('Апрель', 4),
        ('Май', 5), ('Июнь', 6), ('Июль', 7), ('Август', 8),
        ('Сентябрь', 9), ('Октябрь', 10), ('Ноябрь', 11), ('Декабрь', 12),
    ]
    SUBJECTS = [
        ('Информатика', 1), ('Математика профильная', 2), ('Математика базовая', 3), ('Математика', 4),
        ('Физика', 5), ('Русский язык', 6), ('Английский язык', 7), ('Литература', 8),
        ('Биология', 9), ('Химия', 10), ('История', 11), ('Обществознание', 12),
    ]
    title = models.CharField(max_length=200, verbose_name='Название курса')
    content = models.TextField(blank=True, verbose_name='Описание курса')
    month = models.CharField(choices=MONTH_CHOICES, verbose_name='Месяц', default='Январь')
    subject = models.CharField(choices=SUBJECTS, verbose_name='Название предмета', default='Информатика')
    students = models.ManyToManyField(User, related_name='courses', blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Учитель курса')
    
    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, verbose_name='Описание урока')
    lesson_date = models.DateField()

    def __str__(self):
        return self.title

class LessonFile(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='lesson_files/')

    def __str__(self):
        return f"File for {self.lesson}"

class Task(models.Model):
    SUBJECTS = [
        ('Информатика', 1), ('Математика профильная', 2), ('Математика базовая', 3), ('Математика', 4),
        ('Физика', 5), ('Русский язык', 6), ('Английский язык', 7), ('Литература', 8),
        ('Биология', 9), ('Химия', 10), ('История', 11), ('Обществознание', 12),
    ]
    question = models.TextField()
    correct_answer = models.CharField(blank=True, max_length=255)
    is_auto = models.BooleanField(default=True)
    ball = models.IntegerField(default=1)
    exam_number = models.IntegerField() 
    subject = models.CharField(choices=SUBJECTS, verbose_name='Название предмета')

    def __str__(self):
        return self.question

class TaskFile(models.Model):
    task = models.ForeignKey(Task, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_files/')

    def __str__(self):
        return f"File for {self.task}"

class Homework(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='homework')
    title = models.CharField(max_length=255)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return self.title

class UserHomeworkResult(models.Model):
    SUBJECTS = [
        ('Информатика', 1), ('Математика профильная', 2), ('Математика базовая', 3), ('Математика', 4),
        ('Физика', 5), ('Русский язык', 6), ('Английский язык', 7), ('Литература', 8),
        ('Биология', 9), ('Химия', 10), ('История', 11), ('Обществознание', 12),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    homework = models.OneToOneField(Homework, on_delete=models.CASCADE, related_name='result')
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField(default=0)
    comment = models.TextField(blank=True)

class UserTaskAnswer(models.Model):
    number = models.IntegerField(default=0)
    homework_result = models.ForeignKey(UserHomeworkResult, on_delete=models.CASCADE, related_name='task_results')
    answers_text = models.CharField(max_length=1023, blank=True)
    correct_answer = models.CharField(max_length=1023, blank=True)
    is_auto = models.BooleanField(default=True)
    result = models.IntegerField(default=0)

class UserTaskAnswerFile(models.Model):
    usertaskanswer = models.ForeignKey(UserTaskAnswer, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='usertaskanswer_files/')

    def __str__(self):
        return f"File for {self.usertaskanswer}"