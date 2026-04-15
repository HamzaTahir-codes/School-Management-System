from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import TimingPreset, TimeSlot, TimetableEntry, Substitution, WorkdayOverride, AttendanceExtension
from academics.models import ClassLevel, Section, TeacherAssignment
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils import timezone

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

# --- Presets ---
class TimingPresetListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = TimingPreset
    template_name = 'timetable/preset_list.html'
    context_object_name = 'presets'
    paginate_by = 10

class TimingPresetCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = TimingPreset
    fields = ['name', 'is_active']
    template_name = 'timetable/generic_form.html'
    success_url = reverse_lazy('timetable:preset_list')

class TimingPresetUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = TimingPreset
    fields = ['name', 'is_active']
    template_name = 'timetable/generic_form.html'
    success_url = reverse_lazy('timetable:preset_list')

# --- Slots ---
class TimeSlotListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = TimeSlot
    template_name = 'timetable/slot_list.html'
    context_object_name = 'slots'
    paginate_by = 10

    def get_queryset(self):
        return TimeSlot.objects.filter(preset_id=self.kwargs['preset_pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['preset'] = get_object_or_404(TimingPreset, pk=self.kwargs['preset_pk'])
        return ctx

class TimeSlotCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = TimeSlot
    fields = ['label', 'start_time', 'end_time', 'slot_type', 'order']
    template_name = 'timetable/generic_form.html'

    def form_valid(self, form):
        form.instance.preset_id = self.kwargs['preset_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('timetable:slot_list', kwargs={'preset_pk': self.kwargs['preset_pk']})

# --- Timetable Builder ---
class TimetableBuilderView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'timetable/builder.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Fetch current class & section from session or GET
        class_pk = self.request.GET.get('class')
        section_pk = self.request.GET.get('section')
        
        ctx['classes'] = ClassLevel.objects.all()
        ctx['active_preset'] = TimingPreset.objects.filter(is_active=True).first()
        ctx['day_names'] = TimetableEntry.Day.choices
        
        if class_pk:
            ctx['selected_class'] = ClassLevel.objects.filter(pk=class_pk).first()
            if section_pk and ctx['selected_class']:
                ctx['selected_section'] = Section.objects.filter(pk=section_pk, class_level=ctx['selected_class']).first()
        
        if ctx.get('selected_section'):
            if ctx['active_preset']:
                slots = ctx['active_preset'].slots.all().order_by('order', 'start_time')
                ctx['has_slots'] = slots.exists()
                
                # Build the grid data
                grid = []
                for slot in slots:
                    row = {'slot': slot, 'days': []}
                    for day_code, day_name in ctx['day_names']:
                        entry = TimetableEntry.objects.filter(
                            day=day_code,
                            timeslot=slot,
                            assignment__section=ctx['selected_section']
                        ).first()
                        row['days'].append({
                            'day_code': day_code,
                            'entry': entry
                        })
                    grid.append(row)
                ctx['grid'] = grid
                
            # For the assignment modal
            ctx['assignments'] = TeacherAssignment.objects.filter(
                section_id=section_pk,
                academic_session__is_current=True
            )
        else:
            ctx['has_slots'] = False
            
        return ctx

def assign_period(request):
    if not request.user.is_authenticated or request.user.role != 'ADMIN':
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        timeslot_id = request.POST.get('timeslot_id')
        day = request.POST.get('day')
        is_attendance = request.POST.get('is_attendance') == 'true'
        
        try:
            assignment = TeacherAssignment.objects.get(pk=assignment_id)
            timeslot = TimeSlot.objects.get(pk=timeslot_id)
            
            with transaction.atomic():
                # If marking as attendance period, unset others for this section/day
                if is_attendance:
                    TimetableEntry.objects.filter(
                        day=day,
                        assignment__section=assignment.section,
                        is_attendance_period=True
                    ).update(is_attendance_period=False)
                
                entry, created = TimetableEntry.objects.update_or_create(
                    day=day,
                    timeslot=timeslot,
                    assignment=assignment,
                    defaults={'is_attendance_period': is_attendance}
                )
                
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def remove_period(request, entry_pk):
    if not request.user.is_authenticated or request.user.role != 'ADMIN':
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    entry = get_object_or_404(TimetableEntry, pk=entry_pk)
    entry.delete()
    return JsonResponse({'success': True})

# --- Substitution ---
class SubstitutionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Substitution
    template_name = 'timetable/sub_list.html'
    context_object_name = 'subs'
    paginate_by = 10

class SubstitutionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Substitution
    fields = ['entry', 'substitute_teacher', 'date', 'reason']
    template_name = 'timetable/generic_form.html'
    success_url = reverse_lazy('timetable:sub_list')

# --- Overrides ---
class WorkdayOverrideListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = WorkdayOverride
    template_name = 'timetable/override_list.html'
    context_object_name = 'overrides'
    paginate_by = 10

class WorkdayOverrideCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = WorkdayOverride
    fields = ['date', 'is_working', 'description']
    template_name = 'timetable/generic_form.html'
    success_url = reverse_lazy('timetable:override_list')

# --- Extension Approval ---
class ExtensionApprovalListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = AttendanceExtension
    template_name = 'timetable/extension_list.html'
    context_object_name = 'extensions'
    paginate_by = 10
    
    def get_queryset(self):
        return AttendanceExtension.objects.all().order_by('-date', '-is_approved')

@login_required
def approve_extension(request, pk):
    if request.user.role != 'ADMIN':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    ext = get_object_or_404(AttendanceExtension, pk=pk)
    ext.is_approved = True
    ext.save()
    
    messages.success(request, f"Extension approved for {ext.teacher}")
    return redirect('timetable:extension_list')

# --- Teacher Views ---
class TeacherScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'timetable/teacher_schedule.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile = getattr(self.request.user, 'teacher_profile', None)
        active_preset = TimingPreset.objects.filter(is_active=True).first()
        
        ctx['active_preset'] = active_preset
        ctx['day_names'] = TimetableEntry.Day.choices
        
        if profile and active_preset:
            slots = active_preset.slots.all().order_by('order', 'start_time')
            
            grid = []
            for slot in slots:
                row = {'slot': slot, 'days': []}
                for day_code, day_name in ctx['day_names']:
                    # Logic: What is this teacher doing at this time?
                    # Check base timetable
                    entry = TimetableEntry.objects.filter(
                        day=day_code,
                        timeslot=slot,
                        assignment__teacher=profile
                    ).first()
                    
                    # Check for substitutions
                    # (Simplified for now: showing the base entry or if they are a substitute)
                    sub = Substitution.objects.filter(
                        substitute_teacher=profile,
                        date=timezone.now().date(),
                        entry__timeslot=slot
                    ).first() if day_code == timezone.now().strftime('%A').upper() else None
                    
                    row['days'].append({
                        'day_code': day_code,
                        'entry': entry,
                        'substitution': sub
                    })
                grid.append(row)
            ctx['grid'] = grid
            ctx['today_name'] = timezone.now().strftime('%A').upper()
            
        return ctx

@login_required
def request_attendance_extension(request):
    if request.method == 'POST' and getattr(request.user, 'role', '') == 'TEACHER':
        section_id = request.POST.get('section_id')
        duration = int(request.POST.get('duration', 15))
        
        try:
            profile = request.user.teacher_profile
            section = Section.objects.get(pk=section_id)
            
            # Create a request
            AttendanceExtension.objects.create(
                teacher=profile,
                section=section,
                date=timezone.now().date(),
                expires_at=timezone.now() + timezone.timedelta(minutes=duration),
                duration_minutes=duration,
                is_approved=False # Admin will approve
            )
            return JsonResponse({'success': True, 'message': 'Request sent to admin.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request'})
