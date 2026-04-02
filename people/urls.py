from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    # Teachers
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('teachers/add/', views.TeacherCreateView.as_view(), name='teacher_add'),
    
    # Parents
    path('parents/', views.ParentListView.as_view(), name='parent_list'),
    path('parents/add/', views.ParentCreateView.as_view(), name='parent_add'),
    
    # Students
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_add'),
]