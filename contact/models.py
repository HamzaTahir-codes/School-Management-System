from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactQuery(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    message = models.TextField()
    
    # Spam prevention tracking
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Contact Query')
        verbose_name_plural = _('Contact Queries')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} - {self.email}"
