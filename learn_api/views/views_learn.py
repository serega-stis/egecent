from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import *
from ..serializers.serializer_learn import *
from django.db.models import Q
from django.db.models import Sum

class CoursesView(generics.ListAPIView):
    serializer_class = CoursesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(students=user)
    

class CourseInfoView(generics.RetrieveAPIView):
    serializer_class = CourseInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(students=user)

class LessonInfoView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

class HomeworkInfoView(generics.RetrieveAPIView):
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()
    permission_classes = [IsAuthenticated]

class TaskView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

class HomeworkSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, home_id):
        homework = Homework.objects.get(pk=home_id)
        if not UserHomeworkResult.objects.filter(homework=homework, user=request.user).exists(): 
            return Response({'Домашка не отправлена'})
        res = UserHomeworkResult.objects.get(homework=homework)
        serializer = HomeworkSubmitSerializer(res)
        return Response(serializer.data)

    def post(self, request, home_id):
        data = request.POST
        files = request.FILES
        if (not data) and (not files): return Response({"Пустая форма отправки"})
        homework = Homework.objects.get(pk=home_id)
        tasks = list(HomeworkSerializer(homework).data['tasks'])
        res = UserHomeworkResult(homework=homework, user=self.request.user)
        res.save()
        for num, ans in data.items():
            task = next(filter(lambda x: int(x.get('number')) == int(num), tasks))
            result_ball = task['ball'] if str(task['correct_answer'].lower()) == str(ans.lower().strip()) else 0
            tasktext = UserTaskAnswer(number=num, 
                                      answers_text=ans, 
                                      homework_result=res,
                                      correct_answer=task['correct_answer'],
                                      result=result_ball)        
            tasktext.save()
        for num, ans in dict(files).items():
            taskfile = UserTaskAnswer(number=num, homework_result=res, is_auto=False)
            taskfile.save()
            for fl in ans:
                utaf = UserTaskAnswerFile(usertaskanswer=taskfile, file=fl)
                utaf.save()
        res.result = res.task_results.aggregate(total=Sum('result'))['total']
        res.save()
        serializer = HomeworkSubmitSerializer(res)
        return Response(serializer.data)

class StateUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        done_homework = UserHomeworkResult.objects.filter(Q(homework__lesson__course__month=request.data['month']) & Q(user=request.user))
        done_ball = sum([rs.result for rs in done_homework])
        all_ball = 0
        for ush in done_homework:
            all_ball += sum([tk.ball for tk in ush.homework.tasks.all()])
        all_homework = 0
        for cr in Course.objects.filter(students=request.user):
            for ls in cr.lessons.all():
                if ls.homework != None:
                    all_homework += 1
        procent = int(done_ball / all_ball * 100)
        if procent >= 80: grade = 5
        elif procent >= 50: grade = 4 
        elif procent >= 20: grade = 3
        else: grade = 2
        state = {
            'all_count_homework': all_homework,
            'done_count_homework': len(done_homework),
            'all_ball': all_ball,
            'done_ball': done_ball,
            'procent': procent,
            'grade': grade
        }
        return(Response(state))
    
class SelectedTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        st, created = SelectedTasks.objects.get_or_create(user=user)
        st.tasks.add(Task.objects.get(pk=request.data['task']))

        serializer = SelectedTasksSerializer(st)
        st.save()
        return Response(serializer.data)
    
    def get(self, request):
        user = request.user
        st, created = SelectedTasks.objects.get_or_create(user=user)
        serializer = SelectedTasksSerializer(st)
        st.save()
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        st, created = SelectedTasks.objects.get_or_create(user=user)
        who_del = Task(pk=request.data['task'])
        st.tasks.remove(who_del)
        serializer = SelectedTasksSerializer(st)
        st.save()
        return Response(serializer.data)