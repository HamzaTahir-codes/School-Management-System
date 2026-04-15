from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class TimingPreset(models.Model):
    name = models.CharField(max_length=100)  # Summer, Winter, Ramzan, Normal
    is_active = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.is_active:
            TimingPreset.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    class SlotType(models.TextChoices):
        PERIOD = 'PERIOD', 'Academic Period'
        BREAK = 'BREAK', 'Break/Recess'
        ASSEMBLY = 'ASSEMBLY', 'Assembly'
        OTHER = 'OTHER', 'Other'

    preset = models.ForeignKey(TimingPreset, on_delete=models.CASCADE, related_name='slots')
    label = models.CharField(max_length=50)  # 1st Period, Lunch Break
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_type = models.CharField(max_length=20, choices=SlotType.choices, default=SlotType.PERIOD)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['order', 'start_time']

    def __str__(self):
        return f"{self.label} ({self.start_time} - {self.end_time})"

class TimetableEntry(models.Model):
    class Day(models.TextChoices):
        MONDAY = 'MONDAY', 'Monday'
        TUESDAY = 'TUESDAY', 'Tuesday'
        WEDNESDAY = 'WEDNESDAY', 'Wednesday'
        THURSDAY = 'THURSDAY', 'Thursday'
        FRIDAY = 'FRIDAY', 'Friday'
        SATURDAY = 'SATURDAY', 'Saturday'
        SUNDAY = 'SUNDAY', 'Sunday'

    day = models.CharField(max_length=10, choices=Day.choices)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='entries')
    assignment = models.ForeignKey('academics.TeacherAssignment', on_delete=models.CASCADE, related_name='timetable_entries')
    room = models.CharField(max_length=50, blank=True, null=True)
    is_attendance_period = models.BooleanField(default=False)

    class Meta:
        unique_together = ('day', 'timeslot', 'assignment')

    def clean(self):
        # 1. Teacher Clash
        teacher = self.assignment.teacher
        clashing_teacher = TimetableEntry.objects.filter(
            day=self.day,
            timeslot=self.timeslot,
            assignment__teacher=teacher
        ).exclude(pk=self.pk).first()
        
        if clashing_teacher:
            raise ValidationError(f"Teacher {teacher} is already assigned to {clashing_teacher.assignment.subject} in {clashing_teacher.assignment.section} during {self.timeslot.label}.")

        # 2. Section Clash
        section = self.assignment.section
        clashing_section = TimetableEntry.objects.filter(
            day=self.day,
            timeslot=self.timeslot,
            assignment__section=section
        ).exclude(pk=self.pk).first()
        
        if clashing_section:
            raise ValidationError(f"Section {section} already has {clashing_section.assignment.subject} with {clashing_section.assignment.teacher} during {self.timeslot.label}.")

        # 3. Room Clash
        if self.room:
            clashing_room = TimetableEntry.objects.filter(
                day=self.day,
                timeslot=self.timeslot,
                room=self.room
            ).exclude(pk=self.pk).first()
            if clashing_room:
                raise ValidationError(f"Room {self.room} is already occupied by {clashing_room.assignment.section} during {self.timeslot.label}.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.day} - {self.timeslot.label} - {self.assignment}"

class Substitution(models.Model):
    entry = models.ForeignKey(TimetableEntry, on_delete=models.CASCADE, related_name='substitutions')
    substitute_teacher = models.ForeignKey('people.TeacherProfile', on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sub for {self.entry} on {self.date}"

class AttendanceExtension(models.Model):
    teacher = models.ForeignKey('people.TeacherProfile', on_delete=models.CASCADE)
    section = models.ForeignKey('academics.Section', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    expires_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(help_text="Selected via Admin badges (15, 30, 60)")
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Extension for {self.teacher} on {self.date}"

class WorkdayOverride(models.Model):
    date = models.DateField(unique=True)
    is_working = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True, help_text="e.g. Working Saturday or Unexpected Holiday")

    def __str__(self):
        status = "Working" if self.is_working else "Holiday"
        return f"{self.date}: {status}"
