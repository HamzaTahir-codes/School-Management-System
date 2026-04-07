from django.db import models
from django.utils.translation import gettext_lazy as _

class NotificationLog(models.Model):
    class Category(models.TextChoices):
        FEE_REMINDER = 'FEE', _('Fee Reminder')
        ATTENDANCE = 'ATTENDANCE', _('Attendance Alert')
        BIRTHDAY = 'BIRTHDAY', _('Birthday Wish')
        REPORT = 'REPORT', _('Performance Report')

    recipient = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=Category.choices)
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.recipient}: {self.category}"


class Broadcast(models.Model):
    class Target(models.TextChoices):
        ALL = 'ALL', _('All Roles')
        TEACHER = 'TEACHER', _('Teachers Only')
        STUDENT = 'STUDENT', _('Students Only')
        PARENT = 'PARENT', _('Parents Only')

    title = models.CharField(max_length=200)
    message = models.TextField()
    target_role = models.CharField(max_length=15, choices=Target.choices, default=Target.ALL)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Broadcast: {self.title} ({self.target_role})"


class BroadcastReadStatus(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=True)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'broadcast')


class BroadcastDeleteStatus(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'broadcast')


class CommunicationResponse(models.Model):
    # Response can be to a specific broadcast or a direct notification
    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE, null=True, blank=True, related_name='responses')
    notification = models.ForeignKey(NotificationLog, on_delete=models.CASCADE, null=True, blank=True, related_name='responses')
    
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response from {self.sender} to {self.broadcast or self.notification}"
