from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import TeacherAttendance, StudentAttendance, LeaveRequest
from .forms import TeacherAttendanceForm, StudentAttendanceForm, LeaveRequestForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

class GenericDeleteMixin:
    template_name = 'shared/confirm_delete.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Delete {self.model.__name__}'
        ctx['name'] = str(self.object)
        ctx['back_url'] = self.success_url
        return ctx

# --- Teacher Attendance ---
class TeacherAttendanceListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = TeacherAttendance
    template_name = 'attendance/teacher_attendance_list.html'
    context_object_name = 'records'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Teacher Attendance'
        return ctx

class TeacherAttendanceCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = TeacherAttendance
    form_class = TeacherAttendanceForm
    template_name = 'attendance/generic_form.html'
    success_url = reverse_lazy('attendance:teacher_attendance_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Log Teacher Attendance'
        ctx['back_url'] = reverse_lazy('attendance:teacher_attendance_list')
        return ctx
    def form_valid(self, form):
        form.instance.marked_by = self.request.user
        messages.success(self.request, "Teacher attendance recorded.")
        return super().form_valid(form)

class TeacherAttendanceUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = TeacherAttendance
    form_class = TeacherAttendanceForm
    template_name = 'attendance/generic_form.html'
    success_url = reverse_lazy('attendance:teacher_attendance_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Teacher Attendance'
        ctx['back_url'] = reverse_lazy('attendance:teacher_attendance_list')
        return ctx

class TeacherAttendanceDeleteView(LoginRequiredMixin, AdminRequiredMixin, GenericDeleteMixin, DeleteView):
    model = TeacherAttendance
    success_url = reverse_lazy('attendance:teacher_attendance_list')

# --- Student Attendance ---
class StudentAttendanceListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = StudentAttendance
    template_name = 'attendance/student_attendance_list.html'
    context_object_name = 'records'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Student Attendance'
        return ctx

class StudentAttendanceCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = StudentAttendance
    form_class = StudentAttendanceForm
    template_name = 'attendance/generic_form.html'
    success_url = reverse_lazy('attendance:student_attendance_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Log Student Attendance'
        ctx['back_url'] = reverse_lazy('attendance:student_attendance_list')
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Student attendance recorded.")
        return super().form_valid(form)

class StudentAttendanceUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = StudentAttendance
    form_class = StudentAttendanceForm
    template_name = 'attendance/generic_form.html'
    success_url = reverse_lazy('attendance:student_attendance_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Student Attendance'
        ctx['back_url'] = reverse_lazy('attendance:student_attendance_list')
        return ctx

class StudentAttendanceDeleteView(LoginRequiredMixin, AdminRequiredMixin, GenericDeleteMixin, DeleteView):
    model = StudentAttendance
    success_url = reverse_lazy('attendance:student_attendance_list')

# --- Leave Requests ---
class LeaveRequestListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'attendance/leave_request_list.html'
    context_object_name = 'requests'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Leave Requests'
        return ctx

class LeaveRequestCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'attendance/generic_form.html'
    success_url = reverse_lazy('attendance:leave_request_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Submit Leave Request'
        ctx['back_url'] = reverse_lazy('attendance:leave_request_list')
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Leave request logged.")
        return super().form_valid(form)

class LeaveRequestUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'attendance/generic_form.html'
    success_url = reverse_lazy('attendance:leave_request_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Leave Request'
        ctx['back_url'] = reverse_lazy('attendance:leave_request_list')
        return ctx

class LeaveRequestDeleteView(LoginRequiredMixin, AdminRequiredMixin, GenericDeleteMixin, DeleteView):
    model = LeaveRequest
    success_url = reverse_lazy('attendance:leave_request_list')
