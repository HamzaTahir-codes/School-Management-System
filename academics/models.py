from django.db import models
class AcademicSession(models.Model):
    name = models.CharField(max_length=50)  # e.g., 2025-2026
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicSession.objects.filter(
                school=self.school, is_current=True
            ).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ClassLevel(models.Model):
    name = models.CharField(max_length=50)  # e.g., Grade 10, Class 5
    numeric_value = models.PositiveIntegerField()

    class Meta:
        unique_together = ('name',)

    def __str__(self):
        return self.name


class Section(models.Model):
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=10)  # A, B, C
    capacity = models.PositiveIntegerField(default=80)

    class Meta:
        unique_together = ('class_level', 'name')

    def __str__(self):
        return f"{self.class_level} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} ({self.code})"