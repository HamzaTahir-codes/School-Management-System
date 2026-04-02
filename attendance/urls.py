from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Teacher Attendance
    path('teachers/', views.TeacherAttendanceListView.as_view(), name='teacher_attendance_list'),
    path('teachers/add/', views.TeacherAttendanceCreateView.as_view(), name='teacher_attendance_add'),
    
    # Student Attendance
    path('students/', views.StudentAttendanceListView.as_view(), name='student_attendance_list'),
    path('students/add/', views.StudentAttendanceCreateView.as_view(), name='student_attendance_add'),
    
    # Leave Requests
    path('leaves/', views.LeaveRequestListView.as_view(), name='leave_request_list'),
    path('leaves/add/', views.LeaveRequestCreateView.as_view(), name='leave_request_add'),
]