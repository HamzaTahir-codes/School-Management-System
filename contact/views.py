from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import ContactQuery
from notifications.models import NotificationLog
from accounts.models import User

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def submit_query(request):
    if request.method == "POST":
        # Using HTMX, so we return HTML snippets
        
        # 1. Rate Limiting Check
        ip = get_client_ip(request)
        now = timezone.now()
        
        # Check day limit (max 3 per 24h)
        day_ago = now - timedelta(days=1)
        recent_day_count = ContactQuery.objects.filter(ip_address=ip, created_at__gte=day_ago).count()
        
        if recent_day_count >= 3:
            return HttpResponse(
                '<div class="p-4 rounded-xl text-amber-800 bg-amber-50 border border-amber-200">'
                '<strong>Daily Limit Reached:</strong> You have already submitted multiple queries today. Please try again tomorrow.'
                '</div>'
            )
            
        # Check rapid fire limit (1 per 5 mins)
        five_mins_ago = now - timedelta(minutes=5)
        recent_5min = ContactQuery.objects.filter(ip_address=ip, created_at__gte=five_mins_ago).exists()
        
        if recent_5min:
            return HttpResponse(
                '<div class="p-4 rounded-xl text-amber-800 bg-amber-50 border border-amber-200">'
                '<strong>Too Many Requests:</strong> Please wait a few minutes before submitting another query.'
                '</div>'
            )

        # 2. Extract Data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not first_name or not email or not message:
            return HttpResponse(
                '<div class="p-4 rounded-xl text-rose-800 bg-rose-50 border border-rose-200">'
                'Please fill in all required fields.'
                '</div>'
            )

        # 3. Create Query
        query = ContactQuery.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            message=message,
            ip_address=ip,
            session_key=request.session.session_key
        )

        # 4. Dispatch Notification to ADMINs
        admins = User.objects.filter(role='ADMIN', is_active=True)
        for admin in admins:
            NotificationLog.objects.create(
                recipient=admin,
                category='REPORT',
                message=f"NEW CONTACT QUERY [{email}]\n\n{message}",
                is_sent=True,
                sent_at=now
            )

        # 5. Return Success Template Fragment
        return HttpResponse(
            '<div class="p-8 rounded-3xl text-emerald-800 bg-emerald-50 border border-emerald-200 text-center animate-scale-up shadow-xl">'
            '<div class="mx-auto w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mb-4">'
            '<svg class="w-8 h-8 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>'
            '</div>'
            '<h3 class="text-2xl font-bold mb-2">Message Received!</h3>'
            '<p class="text-emerald-600">Thank you for reaching out. A school administrator will review your query and contact you at <strong>{}</strong> shortly.</p>'
            '</div>'.format(email)
        )

    # Fallback to bad request
    return HttpResponse("Invalid request method.", status=405)
