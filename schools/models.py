from django.db import models
from django.utils import timezone
from datetime import timedelta


class School(models.Model):
    """School / Tenant - Main entity for multi-tenancy"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Unique identifier for the school")
    address = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Subscription & Trial Management
    is_active = models.BooleanField(default=True)
    trial_ends_at = models.DateTimeField(
        default=timezone.now() + timedelta(days=2),
        help_text="Trial period ends after 2 days by default"
    )
    subscription_plan = models.CharField(
        max_length=50,
        default='trial',
        choices=[
            ('trial', 'Trial'),
            ('basic', 'Basic Plan'),
            ('standard', 'Standard Plan'),
            ('premium', 'Premium Plan'),
        ]
    )
    subscription_start_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"
        ordering = ['name']


class SchoolSubscriptionPayment(models.Model):
    """Payments made by schools for their subscription"""
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='subscription_payments'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount paid in PKR or chosen currency"
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Payment gateway transaction ID (e.g., Stripe, JazzCash, EasyPaisa)"
    )
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('stripe', 'Stripe'),
            ('jazzcash', 'JazzCash'),
            ('easypaisa', 'EasyPaisa'),
            ('bank_transfer', 'Bank Transfer'),
            ('other', 'Other'),
        ]
    )
    expiry_date = models.DateField(
        help_text="Subscription expiry date after this payment"
    )
    status = models.CharField(
        max_length=20,
        default='completed',
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('refunded', 'Refunded'),
        ]
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.school.name} - {self.amount} on {self.payment_date.date()}"

    class Meta:
        verbose_name = "School Subscription Payment"
        verbose_name_plural = "School Subscription Payments"
        ordering = ['-payment_date']
        indexes = [
            models.Index(fields=['school', 'payment_date']),
            models.Index(fields=['transaction_id']),
        ]