from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('teachers/', views.TeacherAttendanceListView.as_view(), name='teacher_attendance_list'),
    path('teachers/add/', views.TeacherAttendanceCreateView.as_view(), name='teacher_attendance_add'),
    path('teachers/<int:pk>/edit/', views.TeacherAttendanceUpdateView.as_view(), name='teacher_attendance_edit'),
    path('teachers/<int:pk>/delete/', views.TeacherAttendanceDeleteView.as_view(), name='teacher_attendance_delete'),

    path('students/', views.StudentAttendanceListView.as_view(), name='student_attendance_list'),
    path('students/add/', views.StudentAttendanceCreateView.as_view(), name='student_attendance_add'),
    path('students/<int:pk>/edit/', views.StudentAttendanceUpdateView.as_view(), name='student_attendance_edit'),
    path('students/<int:pk>/delete/', views.StudentAttendanceDeleteView.as_view(), name='student_attendance_delete'),

    path('leaves/', views.LeaveRequestListView.as_view(), name='leave_request_list'),
    path('leaves/add/', views.LeaveRequestCreateView.as_view(), name='leave_request_add'),
    path('leaves/<int:pk>/edit/', views.LeaveRequestUpdateView.as_view(), name='leave_request_edit'),
    path('leaves/<int:pk>/delete/', views.LeaveRequestDeleteView.as_view(), name='leave_request_delete'),
]