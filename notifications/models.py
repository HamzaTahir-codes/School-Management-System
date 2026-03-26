from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TenantModel


class NotificationLog(TenantModel):
    class Category(models.TextChoices):
        FEE_REMINDER = 'FEE', _('Fee Reminder')
        ATTENDANCE = 'ATTENDANCE', _('Attendance Alert')
        BIRTHDAY = 'BIRTHDAY', _('Birthday Wish')
        REPORT = 'REPORT', _('Performance Report')

    recipient = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=Category.choices)
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)