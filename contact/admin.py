from django.contrib import admin
from .models import ContactQuery

@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at', 'is_read', 'ip_address')
    list_filter = ('is_read', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'message')
    readonly_fields = ('first_name', 'last_name', 'email', 'message', 'ip_address', 'session_key', 'created_at')
    ordering = ('-created_at',)
