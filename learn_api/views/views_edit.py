from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.views import APIView
from ..models import *
from ..serializers.serializer_edit import *
from ..permissions import IsTeacher, IsAdmin
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated


class CourseEditView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsTeacher, IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Course.objects.all()
        return Course.objects.filter(teacher=self.request.user)


class LessonEditView(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsTeacher, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        raise exceptions.NotFound(detail="Список уроков недоступен.")

class HomeworkEditView(viewsets.ModelViewSet):
    serializer_class = HomeworkSerializerEdit
    queryset = Homework.objects.all()
    permission_classes = [IsTeacher, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        raise exceptions.NotFound(detail="Список домашек недоступен.")

class UserHomeworkView(generics.ListAPIView):
    serializer_class = UserHomeworkSerializer
    queryset = UserHomeworkResult.objects.all()
    permission_classes = [IsTeacher, IsAuthenticated]


class UserHomeworkInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = UserHomeworkInfoSerializer
    queryset = UserHomeworkResult.objects.all()
    permission_classes = [IsTeacher, IsAuthenticated]

class TaskEditView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_permissions(self):
        if self.action == 'delete':
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsTeacher]
        return [permission() for permission in permission_classes]


class RateAnswerView(APIView):
    permission_classes = [IsTeacher, IsAuthenticated]

    def patch(self, request, res_id):
        change = {}
        for key, value in request.data.items():
            if key == 'comment':
                ts = UserHomeworkResult.objects.get(pk=res_id)
                ts.comment = value 
                change['comment'] = value
                ts.save()
            else: 
                ts = UserTaskAnswer.objects.get(homework_result__id=res_id, number=key)
                uhr = UserHomeworkResult.objects.get(pk=res_id)
                uhr.result = uhr.task_results.aggregate(total=Sum('result'))['total']
                uhr.save()
                ts.result = value 
                change[key] = value
                ts.save()
        return Response([change])


class UserEditView(viewsets.ReadOnlyModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['post'])
    def get_teacher(self, request):
        teacher = User.objects.get(pk=request.POST.get('id_will_teacher'))
        teacher.is_teacher = True
        teacher.save()
        return Response({f"Пользователь c id {request.POST.get('id_will_teacher')} теперь является учителем!"})
    
    @action(detail=False, methods=['post'])
    def get_admin(self, request):
        adm = User.objects.get(pk=request.POST.get('id_will_admin'))
        adm.is_admin = True
        adm.save()
        return Response({f"Пользователь c id {request.POST.get('id_will_admin')} теперь является администратором!"})


    def get_permissions(self):
        if self.action == 'get_teacher' or self.action == 'get_admin':
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsTeacher]
        return [permission() for permission in permission_classes]
