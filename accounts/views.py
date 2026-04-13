from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User
from .forms import UserUpdateForm
from django.db.models import Q

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
        context['recent_students'] = StudentProfile.objects.select_related('class_level').order_by('-admission_date')[:5]

    elif role == 'TEACHER':
        try:
            profile = request.user.teacher_profile
            context['teacher_profile'] = profile
            context['assignments'] = profile.get_active_assignments()
            context['total_students_managed'] = profile.get_total_students_count()
        except TeacherProfile.DoesNotExist:
            messages.warning(request, "Teacher profile not found. Please contact admin.")

    elif role == 'STUDENT':
        # Students no longer have individual portals/User accounts
        messages.info(request, "Student portal is not available.")
        return redirect('accounts:login')

    elif role == 'PARENT':
        try:
            profile = request.user.parent_profile
            context['parent_profile'] = profile
            context['children'] = profile.children.all().select_related('class_level')
        except ParentProfile.DoesNotExist:
            messages.warning(request, "Parent profile not found.")

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

# --- USER MANAGEMENT (Admin Only) ---

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users_list'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        role_filter = self.request.GET.get('role')
        search_query = self.request.GET.get('q')

        if role_filter:
            queryset = queryset.filter(role=role_filter)
        
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) | 
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        
        return queryset.order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_role = self.request.GET.get('role', '')

        context['roles'] = [
            {
                "code": code,
                "name": name,
                "selected": (code == current_role)
            }
            for code, name in User.Role.choices
        ]

        context['current_role'] = current_role
        context['search_query'] = self.request.GET.get('q', '')

        return context

class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, f"User {form.instance.username} updated successfully.")
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'shared/confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            messages.error(request, "You cannot delete your own admin account.")
            return redirect('accounts:user_list')
        
        messages.success(request, f"User {user.username} and all associated data have been deleted.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Delete User"
        ctx['name'] = f"{self.object.username} ({self.object.role})"
        ctx['warning_message'] = "WARNING: Deleting this user will also delete their profiles (Teacher, Parent, Students) across the entire school system. Review indices carefully before proceeding."
        return ctx