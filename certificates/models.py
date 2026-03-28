from django.db import models
from django.utils.translation import gettext_lazy as _

class Certificate(models.Model):
    class Type(models.TextChoices):
        LEAVING = 'LEAVING', _('School Leaving Certificate')
        MERIT = 'MERIT', _('Merit Certificate')

    student = models.ForeignKey('people.StudentProfile', on_delete=models.CASCADE)
    certificate_type = models.CharField(max_length=20, choices=Type.choices)
    file = models.FileField(upload_to='certificates/%Y/%m/')
    issued_at = models.DateTimeField(auto_now_add=True)