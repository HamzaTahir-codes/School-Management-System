from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
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
    paginate_by = 10
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
    is_within_window = False
    
    if settings.start_time <= settings.end_time:
        # Standard window within a single day
        is_within_window = settings.start_time <= current_time <= settings.end_time
    else:
        # Window crosses midnight (e.g., 23:30 to 00:30)
        is_within_window = current_time >= settings.start_time or current_time <= settings.end_time

    if not is_within_window:
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
    paginate_by = 10
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Student Attendance'
        return ctx

# --- Teacher-Led Student Attendance (Timetable Integrated) ---
@login_required
def mark_students_attendance(request):
    """
    Highly secure and timetable-integrated marking view.
    Ensures:
    1. Teacher is authorized (assigned to this section/day as Attendance period).
    2. Today is a working day.
    3. Current time is within the Slot duration OR an extension exists.
    """
    if getattr(request.user, 'role', '') != 'TEACHER':
        messages.error(request, "Only teachers can access the marking portal.")
        return redirect('accounts:dashboard')

    from academics.models import Section, ClassLevel
    from people.models import StudentProfile
    from timetable.models import TimetableEntry, WorkdayOverride, AttendanceExtension
    
    class_pk = request.GET.get('class')
    section_pk = request.GET.get('section')
    
    if not class_pk or not section_pk:
        messages.error(request, "Invalid class or section selected.")
        return redirect('accounts:dashboard')
        
    section = get_object_or_404(Section, pk=section_pk)
    profile = request.user.teacher_profile
    today = timezone.localtime().date()
    now_time = timezone.localtime().time()
    today_name = today.strftime('%A').upper()
    
    # --- 1. Authorized Check ---
    # Find the Timetable entry for this teacher, section, and day which is designated as Attendance period
    att_entry = TimetableEntry.objects.filter(
        day=today_name,
        assignment__teacher=profile,
        assignment__section=section,
        is_attendance_period=True
    ).first()
    
    if not att_entry:
        messages.error(request, f"You are not designated to mark attendance for {section} today.")
        return redirect('accounts:dashboard')
        
    # --- 2. Working Day Check ---
    is_working = True
    override = WorkdayOverride.objects.filter(date=today).first()
    if override:
        is_working = override.is_working
    elif today_name in ['SATURDAY', 'SUNDAY']:
        is_working = False
        
    if not is_working:
        messages.error(request, "Today is marked as a holiday.")
        return redirect('accounts:dashboard')

    # --- 3. Timing Window Check ---
    is_in_window = att_entry.timeslot.start_time <= now_time <= att_entry.timeslot.end_time
    has_extension = AttendanceExtension.objects.filter(
        teacher=profile,
        section=section,
        date=today,
        is_approved=True,
        expires_at__gt=timezone.now()
    ).exists()
    
    if not (is_in_window or has_extension):
        messages.error(request, f"Attendance window ( {att_entry.timeslot.start_time.strftime('%H:%M')} - {att_entry.timeslot.end_time.strftime('%H:%M')} ) has passed.")
        return redirect('accounts:dashboard')

    # --- 4. Render Grid ---
    students = StudentProfile.objects.filter(section=section, status='ACTIVE').order_by('roll_number')
    
    # Get already marked attendance for today
    marked_today = StudentAttendance.objects.filter(date=today, student__section=section).values_list('student_id', 'is_present')
    marked_dict = {s_id: is_p for s_id, is_p in marked_today}

    context = {
        'section': section,
        'students': students,
        'marked_dict': marked_dict,
        'today': today,
        'timeslot': att_entry.timeslot
    }
    return render(request, 'attendance/mark_students_attendance.html', context)

@login_required
def toggle_student_attendance(request):
    """AJAX toggler for the Visual Roll Call grid"""
    if request.method != 'POST' or getattr(request.user, 'role', '') != 'TEACHER':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    student_id = request.POST.get('student_id')
    is_present = request.POST.get('is_present') == 'true'
    today = timezone.localtime().date()
    
    from people.models import StudentProfile
    student = get_object_or_404(StudentProfile, pk=student_id)
    
    # Record or Update
    att, created = StudentAttendance.objects.update_or_create(
        student=student,
        date=today,
        defaults={'is_present': is_present, 'teacher': request.user.teacher_profile}
    )
    
    return JsonResponse({'success': True, 'is_present': att.is_present})

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
    paginate_by = 10
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

