from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import TeacherAttendance, StudentAttendance, LeaveRequest
from .forms import TeacherAttendanceForm, StudentAttendanceForm, LeaveRequestForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

# --- Teacher Attendance ---
class TeacherAttendanceListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = TeacherAttendance
    template_name = 'attendance/teacher_attendance_list.html'
    context_object_name = 'records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Teacher Attendance'
        return context

class TeacherAttendanceCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = TeacherAttendance
    form_class = TeacherAttendanceForm
    template_name = 'attendance/generic_form.html'
    success_url = reverse_lazy('attendance:teacher_attendance_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log Teacher Attendance'
        context['back_url'] = reverse_lazy('attendance:teacher_attendance_list')
        return context

    def form_valid(self, form):
        form.instance.marked_by = self.request.user
        messages.success(self.request, "Teacher attendance successfully recorded.")
        return super().form_valid(form)


# --- Student Attendance ---
class StudentAttendanceListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = StudentAttendance
    template_name = 'attendance/student_attendance_list.html'
    context_object_name = 'records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student Attendance'
        return context

class StudentAttendanceCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = StudentAttendance
    form_class = StudentAttendanceForm
    template_name = 'attendance/generic_form.html'
    success_url = reverse_lazy('attendance:student_attendance_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log Student Attendance'
        context['back_url'] = reverse_lazy('attendance:student_attendance_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Student attendance successfully recorded.")
        return super().form_valid(form)


# --- Leave Requests ---
class LeaveRequestListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'attendance/leave_request_list.html'
    context_object_name = 'requests'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Leave Requests'
        return context

class LeaveRequestCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'attendance/generic_form.html'
    success_url = reverse_lazy('attendance:leave_request_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Submit Leave Request'
        context['back_url'] = reverse_lazy('attendance:leave_request_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Leave Request securely logged.")
        return super().form_valid(form)
