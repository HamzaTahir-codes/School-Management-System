from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import TeacherAttendance, StudentAttendance, LeaveRequest, AttendanceSettings, TeacherAttendanceOTP
from .forms import TeacherAttendanceForm, StudentAttendanceForm, LeaveRequestForm, AttendanceSettingsForm
from django.http import JsonResponse
from django.utils import timezone
import ipaddress
import random
from datetime import timedelta

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

from django.shortcuts import render, redirect

def index(request):
    if not request.user.is_authenticated or request.user.role != 'ADMIN':
        messages.error(request, 'You are not authorized to visit this page.')
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return redirect('school_index')
    return render(request, 'attendance/index.html')

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

@login_required
def initiate_teacher_attendance(request):
    if request.method != 'POST' or getattr(request.user, 'role', '') != 'TEACHER':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        profile = request.user.teacher_profile
    except Exception:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)

    settings = AttendanceSettings.objects.first()
    if not settings:
        return JsonResponse({'error': 'Attendance is not configured yet.'}, status=400)

    # 1. Time Check
    current_time = timezone.localtime().time()
    if not (settings.start_time <= current_time <= settings.end_time):
        return JsonResponse({'error': f'Attendance marking is only allowed between {settings.start_time.strftime("%H:%M")} and {settings.end_time.strftime("%H:%M")}.'}, status=400)

    # 2. Network Check
    # Handle X-Forwarded-For if behind a proxy like ngrok
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        request_ip = x_forwarded_for.split(',')[0].strip()
    else:
        request_ip = request.META.get('REMOTE_ADDR')

    try:
        client_ip = ipaddress.ip_address(request_ip)
        allowed_network = ipaddress.ip_network(settings.allowed_ip_network, strict=False)
        if client_ip not in allowed_network:
            return JsonResponse({'error': 'You must be connected to the school network to mark attendance.'}, status=403)
    except ValueError:
        return JsonResponse({'error': 'Unable to determine or validate your IP address.'}, status=400)
    
    # 3. Rate limiting Check (max 3 per minute)
    one_min_ago = timezone.now() - timedelta(minutes=1)
    recent_otps = TeacherAttendanceOTP.objects.filter(teacher=profile, created_at__gte=one_min_ago).count()
    if recent_otps >= 3:
        return JsonResponse({'error': 'Too many requests. Please wait a minute.'}, status=429)

    # All checks passed, generate OTP
    otp_code = str(random.randint(100000, 999999))
    expires = timezone.now() + timedelta(seconds=60)
    
    TeacherAttendanceOTP.objects.create(
        teacher=profile,
        otp=otp_code,
        expires_at=expires,
        request_ip=request_ip
    )

    return JsonResponse({
        'success': True,
        'message': 'OTP generated successfully.',
        'otp': otp_code
    })

@login_required
def verify_teacher_attendance(request):
    if request.method != 'POST' or getattr(request.user, 'role', '') != 'TEACHER':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        profile = request.user.teacher_profile
    except Exception:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)

    otp_input = request.POST.get('otp', '').strip()
    device_id_input = request.POST.get('device_id', '').strip()

    if not otp_input or not device_id_input:
        return JsonResponse({'error': 'Missing OTP or Device ID'}, status=400)

    # Validate Device Binding
    if profile.registered_device_id:
        if profile.registered_device_id != device_id_input:
            return JsonResponse({'error': 'Unrecognized device. Please use your registered device or contact admin to reset.'}, status=403)
    else:
        # First time marking attendance, bind device
        profile.registered_device_id = device_id_input
        profile.save(update_fields=['registered_device_id'])

    # Validate OTP
    otp_record = TeacherAttendanceOTP.objects.filter(
        teacher=profile,
        otp=otp_input,
        is_used=False
    ).order_by('-created_at').first()

    if not otp_record:
        return JsonResponse({'error': 'Invalid OTP.'}, status=400)

    if timezone.now() > otp_record.expires_at:
        return JsonResponse({'error': 'OTP has expired. Please initiate again.'}, status=400)

    # Mark as used
    otp_record.is_used = True
    otp_record.save(update_fields=['is_used'])

    # Record Attendance
    today = timezone.localtime().date()
    att, created = TeacherAttendance.objects.get_or_create(
        teacher=profile,
        date=today,
        defaults={
            'is_present': True,
            'verified_by_otp': True,
            'ip_address': otp_record.request_ip,
            'device_id': device_id_input
        }
    )

    if not created:
        return JsonResponse({'error': 'Attendance already marked for today.'}, status=400)

    return JsonResponse({'success': True, 'message': 'Attendance marked successfully.'})

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

# --- Administration ---
class AttendanceSettingsUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = AttendanceSettings
    form_class = AttendanceSettingsForm
    template_name = 'attendance/generic_form.html'
    success_url = reverse_lazy('attendance:settings')

    def get_object(self, queryset=None):
        obj, created = AttendanceSettings.objects.get_or_create(id=1)
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Attendance Settings'
        ctx['back_url'] = reverse_lazy('attendance:teacher_attendance_list')
        
        # Get client IP for easier setup
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0].strip()
        else:
            client_ip = self.request.META.get('REMOTE_ADDR')
        
        ctx['client_ip'] = client_ip
        ctx['help_text'] = f"Your current detected IP is: {client_ip}. You can use this to configure the allowed network (e.g., {client_ip}/32)."
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Attendance settings updated successfully.")
        return super().form_valid(form)

from django.views.generic import View
from django.shortcuts import get_object_or_404
from people.models import TeacherProfile

class ResetTeacherDeviceView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(TeacherProfile, pk=pk)
        teacher.registered_device_id = None
        teacher.save(update_fields=['registered_device_id'])
        messages.success(request, f"Device ID reset for {teacher.user.get_full_name()}. They can now bind a new device on their next attendance login.")
        return redirect('people:teacher_detail', pk=teacher.pk)

