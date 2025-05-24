from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from learn_api.views.views_learn import *
from learn_api.views.views_edit import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

learn_paths = [
    path('courses/', CoursesView.as_view()),
    path('courses/<int:pk>/', CourseInfoView.as_view()),
    path('lesson/<int:pk>/', LessonInfoView.as_view()),
    path('homework/<int:pk>/', HomeworkInfoView.as_view()),
    path('tasks/<int:pk>/', TaskView.as_view()),
    path('homework/<int:home_id>/submit/', HomeworkSubmitView.as_view()),
    path('stateuser/', StateUser.as_view()),
    path('selectedtasks/', SelectedTasksView.as_view()),
]

edit_paths_router = DefaultRouter()
edit_paths_router.register(r'course', CourseEditView, basename='course')
edit_paths_router.register(r'lesson', LessonEditView)
edit_paths_router.register(r'task', TaskEditView)
edit_paths_router.register(r'homework', HomeworkEditView)
edit_paths_router.register(r'user', UserEditView)

edit_paths = [
    path('user-homework/', UserHomeworkView.as_view()),
    path('user-homework/<int:pk>/', UserHomeworkInfoView.as_view()),
    path('user-homework/<int:res_id>/rate/', RateAnswerView.as_view()),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/learn/', include(learn_paths)),
    path('api/v1/edit/', include(edit_paths_router.urls)),
    path('api/v1/edit/', include(edit_paths)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
