from django.urls import path
from . import views

app_name = 'attendance'

print("DEBUG: Loading attendance.urls")
urlpatterns = [
    path('', views.index, name='index'),
    path('teachers/', views.TeacherAttendanceListView.as_view(), name='teacher_attendance_list'),
    path('teachers/mark/initiate/', views.initiate_teacher_attendance, name='teacher_attendance_initiate'),
    path('teachers/mark/verify/', views.verify_teacher_attendance, name='teacher_attendance_verify'),

    path('students/', views.StudentAttendanceListView.as_view(), name='student_attendance_list'),
    path('students/add/', views.StudentAttendanceCreateView.as_view(), name='student_attendance_add'),
    path('students/<int:pk>/edit/', views.StudentAttendanceUpdateView.as_view(), name='student_attendance_edit'),
    path('students/<int:pk>/delete/', views.StudentAttendanceDeleteView.as_view(), name='student_attendance_delete'),

    path('leaves/', views.LeaveRequestListView.as_view(), name='leave_request_list'),
    path('leaves/add/', views.LeaveRequestCreateView.as_view(), name='leave_request_add'),
    path('leaves/<int:pk>/edit/', views.LeaveRequestUpdateView.as_view(), name='leave_request_edit'),
    path('leaves/<int:pk>/delete/', views.LeaveRequestDeleteView.as_view(), name='leave_request_delete'),

    path('settings/', views.AttendanceSettingsUpdateView.as_view(), name='settings'),
    path('teachers/<int:pk>/reset-device/', views.ResetTeacherDeviceView.as_view(), name='teacher_reset_device'),
]