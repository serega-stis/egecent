from rest_framework import serializers
from ..models import *


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'month', 'subject']

class LessonFilesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = LessonFile
        fields = ['file']

class LessonSerializer(serializers.ModelSerializer):
    homework = serializers.PrimaryKeyRelatedField(read_only=True)
    files = LessonFilesSerializer(many=True, required=False)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'homework', 'course', 'files']

    def create(self, validated_data):
        files_data = self.context.get('request').FILES.getlist('files')
        lesson = Lesson.objects.create(**validated_data)
        if files_data:
            for file_data in files_data:
                LessonFile.objects.create(lesson=lesson, file=file_data)
        return lesson

    def update(self, instance, validated_data):
        files_data = self.context.get('request').FILES.getlist('files')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if files_data:
            try: 
                LessonFile.objects.filter(lesson=instance).delete()
            except:
                pass
            for file_data in files_data:
                LessonFile.objects.create(lesson=instance, file=file_data)
        return instance
        


class CourseInfoSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'content', 'month', 'teacher', 'subject', 'lessons']


class HomeworkSerializer(serializers.ModelSerializer):
    is_done = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Homework
        fields = ['id', 'title', 'tasks', 'is_done']

    def get_tasks(self, obj):
        tasks = obj.tasks.all()
        serializer = TaskSerializer(tasks, many=True, context={'tasks': tasks})
        return serializer.data

    def get_is_done(self, obj):
        try: 
            return UserHomeworkResult.objects.filter(homework=obj, user=self.context['request'].user).exists()
        except: 
            return False


class TaskFilesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TaskFile
        fields = ['file']

class TaskSerializer(serializers.ModelSerializer):
    number = serializers.SerializerMethodField()
    files = TaskFilesSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'question', 'correct_answer', 'ball', 'is_auto', 'number', 'files']

    def get_number(self, obj):
        try:
            tasks = self.context.get('tasks', [])
            return list(tasks).index(obj) + 1
        except:
            return 0
        
    def create(self, validated_data):
        files_data = self.context.get('request').FILES.getlist('files')
        task = Task.objects.create(**validated_data)
        if files_data:
            for file_data in files_data:
                TaskFile.objects.create(task=task, file=file_data)
        return task

    def update(self, instance, validated_data):

        files_data = self.context.get('request').FILES.getlist('files')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if files_data:
            try: 
                TaskFile.objects.filter(task=instance).delete()
            except:
                pass
            for file_data in files_data:
                TaskFile.objects.create(task=instance, file=file_data)
        return instance
    

class UserTaskAnswerFilesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserTaskAnswerFile
        fields = ['id', 'file']

class UserTaskAnswerSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    files = UserTaskAnswerFilesSerializer(many=True, required=False)
    
    class Meta: 
        model = UserTaskAnswer
        fields = ['number', 'answers_text', 'files', 'question', 'correct_answer', 'is_auto', 'result']

    def get_question(self, obj):
        ts = TaskSerializer(obj.homework_result.homework.tasks.all(), many=True, context={'tasks': obj.homework_result.homework.tasks.all()}).data
        for t in ts:
            if obj.number == t['number']:
                return t['question']
            

    def create(self, validated_data):
        files_data = self.context.get('request').FILES.getlist('files')
        usertaskanswer = UserTaskAnswer.objects.create(**validated_data)
        if files_data:
            for file_data in files_data:
                UserTaskAnswerFile.objects.create(usertaskanswer=usertaskanswer, file=file_data)
        return usertaskanswer

    def update(self, instance, validated_data):
        files_data = self.context.get('request').FILES.getlist('files')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if files_data:
            try: 
                UserTaskAnswerFile.objects.filter(usertaskanswer=instance).delete()
            except:
                pass
            for file_data in files_data:
                UserTaskAnswerFile.objects.create(usertaskanswer=instance, file=file_data)
        return instance
            



class HomeworkSubmitSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = UserHomeworkResult
        fields = ['created_at', 'result', 'comment', 'answers']

    def get_answers(self, obj):
        return UserTaskAnswerSerializer(obj.task_results.all(), many=True).data


class HomeworkResultSerializer(serializers.ModelSerializer):
    correct_answers = serializers.SerializerMethodField()
    tasks_id = serializers.SerializerMethodField()
    
    
    class Meta: 
        model = UserHomeworkResult
        fields = ['answers', 'created_at', 'correct_answers', 'result', 'tasks_id']

    def get_correct_answers(self, obj):
        return {str(task.id): task.correct_answer for task in obj.homework.tasks.all()}
    
    def get_tasks_id(self, obj):
        return [str(task.id) for task in obj.homework.tasks.all()]