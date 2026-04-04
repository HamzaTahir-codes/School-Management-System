from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
class CustomLoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

from django.db.models import Sum, Count
from people.models import TeacherProfile, StudentProfile, ParentProfile
from fees.models import StudentFeePayment
from academics.models import ClassLevel
from attendance.models import StudentAttendance, LeaveRequest
from django.utils import timezone

@login_required
def dashboard_view(request):
    role = request.user.role
    context = {
        'role': role,
        'user': request.user
    }

    if role == 'ADMIN':
        # Stats for Admin
        context['total_students'] = StudentProfile.objects.count()
        context['total_teachers'] = TeacherProfile.objects.count()
        context['total_parents'] = ParentProfile.objects.count()
        
        # Monthly Revenue (Confirmed payments in the current month)
        today = timezone.now().date()
        current_month = today.month
        context['monthly_revenue'] = StudentFeePayment.objects.filter(
            payment_date__month=current_month, 
            is_confirmed=True
        ).aggregate(total=Sum('amount_paid'))['total'] or 0
        
        # Attendance Today
        context['present_today'] = StudentAttendance.objects.filter(date=today, is_present=True).count()
        context['pending_leaves'] = LeaveRequest.objects.filter(status='PENDING').count()
        
        # Chart Data: Students per Class
        class_dist = ClassLevel.objects.annotate(
            student_count=Count('studentprofile')
        ).filter(student_count__gt=0).values('name', 'student_count')
        
        context['chart_labels'] = [item['name'] for item in class_dist]
        context['chart_data'] = [item['student_count'] for item in class_dist]
        
        # Recent activity
        context['recent_students'] = StudentProfile.objects.select_related('user', 'class_level').order_by('-admission_date')[:5]

    return render(request, 'accounts/dashboard.html', context)

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})