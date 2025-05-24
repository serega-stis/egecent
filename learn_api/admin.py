from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  
        (                     
            'Custom Field Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'date_birth',
                    'photo',
                    'is_teacher',
                    'is_admin'
                ),
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Subjects)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(LessonFile)
admin.site.register(Homework)
admin.site.register(Task)
admin.site.register(TaskFile)
admin.site.register(UserHomeworkResult)
admin.site.register(UserTaskAnswer)
admin.site.register(UserTaskAnswerFile)
admin.site.register(SelectedTasks)

