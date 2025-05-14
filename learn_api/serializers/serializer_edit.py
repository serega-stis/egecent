from rest_framework import serializers
from ..models import *
from .serializer_learn import UserTaskAnswerSerializer
from .serializer_learn import TaskSerializer
from .serializer_learn import LessonSerializer

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'content', 'month', 'subject', 'students', 'teacher', 'lessons']


class HomeworkSerializerEdit(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Homework
        fields = ['id', 'tasks', 'title', 'lesson']

    def get_tasks(self, obj):
        tasks = obj.tasks.all()
        serializer = TaskSerializer(tasks, many=True, context={'tasks': tasks})
        return serializer.data
    

    def create(self, validated_data):
        homework = Homework.objects.create(**validated_data)
        tasks = Task.objects.filter(id__in=self.context.get('request').data['tasks'])
        homework.tasks.add(*tasks)
        homework.save()
        return homework

    def update(self, instance, validated_data):
        tasks = Task.objects.filter(id__in=self.context.get('request').data['tasks'])
        instance.tasks.set(tasks)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        


class UserHomeworkSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserHomeworkResult
        fields = ['id', 'user', 'homework', 'course', 'subject', 'teacher', 'created_at', 'result']

    def get_user(self, obj):
        us = UsersSerializer(obj.user).data
        return f"id: {us.get('id')} {us.get('first_name')} {us.get('last_name')}"

    def get_course(self, obj):
        return CourseSerializer(obj.homework.lesson.course).data['title']
    
    def get_subject(self, obj):
        return CourseSerializer(obj.homework.lesson.course).data['subject']

    def get_teacher(self, obj):
        tch = CourseSerializer(obj.homework.lesson.course).data['teacher'] 
        us = UsersSerializer(User.objects.get(id=tch)).data
        return f"id: {us.get('id')} {us.get('first_name')} {us.get('last_name')}" 

class UserHomeworkInfoSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()

    class Meta:
        model = UserHomeworkResult
        fields = ['id', 'user', 'homework', 'answers', 'created_at', 'comment']

    def get_user(self, obj):
        return UsersSerializer(obj.user).data
    
    def get_answers(self, obj):
        return UserTaskAnswerSerializer(obj.task_results.all(), many=True).data

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'date_birth', 'photo', 'is_teacher', 'is_admin']