# school_management/tenant_urls.py
"""
This file is used by ALL tenants (each school).
It contains URLs that should be accessible only after logging into a specific school.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ====================== ADMIN ======================
    path('admin/', admin.site.urls),                    # Each school gets its own admin

    # ====================== AUTHENTICATION ======================
    path('', include('accounts.urls')),      # Login, logout, password change etc.

    # ====================== ACADEMICS ======================
    path('academics/', include('academics.urls', namespace='academics')),

    # ====================== PEOPLE ======================
    path('people/', include('people.urls', namespace='people')),

    # ====================== ATTENDANCE ======================
    path('attendance/', include('attendance.urls', namespace='attendance')),

    # ====================== GRADING & REPORTS ======================
    path('grading/', include('grading.urls', namespace='grading')),

    # ====================== FEES ======================
    path('fees/', include('fees.urls', namespace='fees')),

    # ====================== AI ASSISTANT ======================
    path('ai/', include('ai_assistant.urls', namespace='ai')),

    # ====================== CERTIFICATES ======================
    path('certificates/', include('certificates.urls', namespace='certificates')),

    # ====================== NOTIFICATIONS ======================
    path('notifications/', include('notifications.urls', namespace='notifications')),

    # ====================== API (if you plan to add DRF later) ======================
    # path('api/', include('api.urls', namespace='api')),
]

# Optional: Add a simple home/dashboard redirect
from django.shortcuts import redirect
from django.urls import reverse

def tenant_home(request):
    """Redirect logged-in users to their dashboard"""
    return redirect('dashboard')   # Change to your actual dashboard name

# You can add this if you want a root path for tenants
# urlpatterns = [
#     path('', tenant_home, name='tenant_home'),
# ] + urlpatterns

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)