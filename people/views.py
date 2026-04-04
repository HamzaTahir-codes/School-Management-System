from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.contrib import messages
import random
import string

from accounts.models import User
from .models import TeacherProfile, ParentProfile, StudentProfile
from .forms import (
    TeacherCreationForm, ParentCreationForm, StudentCreationForm,
    TeacherUpdateForm, StudentUpdateForm, ParentUpdateForm,
    BaseUserUpdateForm,
)


def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'


# ===================== BASE CREATE =====================

class BaseProfileCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    def form_valid(self, form):
        with transaction.atomic():
            password = form.cleaned_data.get('password') or generate_random_password()
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=password,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data.get('phone_number', ''),
                role=self.role
            )
            # Save profile picture if provided
            pic = form.cleaned_data.get('profile_picture')
            if pic:
                user.profile_picture = pic
                user.save()
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
        messages.success(self.request, f"{self.role.title()} profile created successfully.")
        return redirect(self.success_url)


# ===================== TEACHERS =====================

class TeacherListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = TeacherProfile
    template_name = 'people/teacher_list.html'
    context_object_name = 'teachers'


class TeacherCreateView(BaseProfileCreateView):
    model = TeacherProfile
    form_class = TeacherCreationForm
    template_name = 'people/teacher_form.html'
    success_url = reverse_lazy('people:teacher_list')
    role = User.Role.TEACHER


class TeacherDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = TeacherProfile
    template_name = 'people/teacher_detail.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object
        context['assignments'] = teacher.assignments.select_related(
            'class_level', 'section', 'subject', 'academic_session'
        ).all()
        from attendance.models import TeacherAttendance
        context['attendance_present'] = TeacherAttendance.objects.filter(teacher=teacher, is_present=True).count()
        context['attendance_absent'] = TeacherAttendance.objects.filter(teacher=teacher, is_present=False).count()
        from grading.models import Mark
        context['recent_marks'] = Mark.objects.filter(teacher=teacher).select_related(
            'student__user', 'subject'
        ).order_by('-id')[:10]
        return context


class TeacherUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = TeacherProfile
    form_class = TeacherUpdateForm
    template_name = 'people/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('people:teacher_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Teacher: {self.object.user.get_full_name()}'
        context['user_form'] = BaseUserUpdateForm(initial={
            'first_name': self.object.user.first_name,
            'last_name': self.object.user.last_name,
            'email': self.object.user.email,
            'phone_number': self.object.user.phone_number,
        })
        context['back_url'] = reverse_lazy('people:teacher_detail', kwargs={'pk': self.object.pk})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        user_form = BaseUserUpdateForm(request.POST, request.FILES)
        if form.is_valid() and user_form.is_valid():
            return self.forms_valid(form, user_form)
        return self.render_to_response(self.get_context_data(form=form))

    def forms_valid(self, form, user_form):
        user = self.object.user
        user.first_name = user_form.cleaned_data['first_name']
        user.last_name = user_form.cleaned_data['last_name']
        user.email = user_form.cleaned_data['email']
        user.phone_number = user_form.cleaned_data['phone_number']
        pic = user_form.cleaned_data.get('profile_picture')
        if pic:
            user.profile_picture = pic
        user.save()
        form.save()
        messages.success(self.request, "Teacher profile updated successfully.")
        return redirect(self.get_success_url())


class TeacherDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = TeacherProfile
    template_name = 'people/confirm_delete.html'
    success_url = reverse_lazy('people:teacher_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Teacher'
        context['name'] = self.object.user.get_full_name() or self.object.user.username
        context['back_url'] = reverse_lazy('people:teacher_detail', kwargs={'pk': self.object.pk})
        return context

    def form_valid(self, form):
        user = self.object.user
        response = super().form_valid(form)
        user.delete()  # Cascade: delete the User account too
        messages.success(self.request, "Teacher and associated account permanently deleted.")
        return response


# ===================== PARENTS =====================

class ParentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ParentProfile
    template_name = 'people/parent_list.html'
    context_object_name = 'parents'


class ParentCreateView(BaseProfileCreateView):
    model = ParentProfile
    form_class = ParentCreationForm
    template_name = 'people/parent_form.html'
    success_url = reverse_lazy('people:parent_list')
    role = User.Role.PARENT


class ParentDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = ParentProfile
    template_name = 'people/parent_detail.html'
    context_object_name = 'parent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['children'] = StudentProfile.objects.filter(parent=self.object).select_related('user', 'class_level', 'section')
        from fees.models import StudentFeePayment
        child_ids = context['children'].values_list('id', flat=True)
        context['payments'] = StudentFeePayment.objects.filter(student_id__in=child_ids).order_by('-payment_date')[:10]
        return context


class ParentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ParentProfile
    form_class = ParentUpdateForm
    template_name = 'people/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('people:parent_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Parent: {self.object.user.get_full_name()}'
        context['user_form'] = BaseUserUpdateForm(initial={
            'first_name': self.object.user.first_name,
            'last_name': self.object.user.last_name,
            'email': self.object.user.email,
            'phone_number': self.object.user.phone_number,
        })
        context['back_url'] = reverse_lazy('people:parent_detail', kwargs={'pk': self.object.pk})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        user_form = BaseUserUpdateForm(request.POST, request.FILES)
        if form.is_valid() and user_form.is_valid():
            return self.forms_valid(form, user_form)
        return self.render_to_response(self.get_context_data(form=form))

    def forms_valid(self, form, user_form):
        user = self.object.user
        user.first_name = user_form.cleaned_data['first_name']
        user.last_name = user_form.cleaned_data['last_name']
        user.email = user_form.cleaned_data['email']
        user.phone_number = user_form.cleaned_data['phone_number']
        pic = user_form.cleaned_data.get('profile_picture')
        if pic:
            user.profile_picture = pic
        user.save()
        form.save()
        messages.success(self.request, "Parent profile updated successfully.")
        return redirect(self.get_success_url())


class ParentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = ParentProfile
    template_name = 'people/confirm_delete.html'
    success_url = reverse_lazy('people:parent_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Parent'
        context['name'] = self.object.user.get_full_name() or self.object.user.username
        context['back_url'] = reverse_lazy('people:parent_detail', kwargs={'pk': self.object.pk})
        return context

    def form_valid(self, form):
        user = self.object.user
        response = super().form_valid(form)
        user.delete()
        messages.success(self.request, "Parent and associated account permanently deleted.")
        return response


# ===================== STUDENTS =====================

class StudentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = StudentProfile
    template_name = 'people/student_list.html'
    context_object_name = 'students'


class StudentCreateView(BaseProfileCreateView):
    model = StudentProfile
    form_class = StudentCreationForm
    template_name = 'people/student_form.html'
    success_url = reverse_lazy('people:student_list')
    role = User.Role.STUDENT


class StudentDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = StudentProfile
    template_name = 'people/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        from attendance.models import StudentAttendance
        context['attendance_present'] = StudentAttendance.objects.filter(student=student, is_present=True).count()
        context['attendance_absent'] = StudentAttendance.objects.filter(student=student, is_present=False).count()
        from grading.models import Mark
        context['marks'] = Mark.objects.filter(student=student).select_related('subject', 'teacher__user', 'academic_session').order_by('subject__name')
        from fees.models import StudentFeePayment
        context['payments'] = StudentFeePayment.objects.filter(student=student).order_by('-payment_date')[:10]
        return context


class StudentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentUpdateForm
    template_name = 'people/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('people:student_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Student: {self.object.user.get_full_name()}'
        context['user_form'] = BaseUserUpdateForm(initial={
            'first_name': self.object.user.first_name,
            'last_name': self.object.user.last_name,
            'email': self.object.user.email,
            'phone_number': self.object.user.phone_number,
        })
        context['back_url'] = reverse_lazy('people:student_detail', kwargs={'pk': self.object.pk})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        user_form = BaseUserUpdateForm(request.POST, request.FILES)
        if form.is_valid() and user_form.is_valid():
            return self.forms_valid(form, user_form)
        return self.render_to_response(self.get_context_data(form=form))

    def forms_valid(self, form, user_form):
        user = self.object.user
        user.first_name = user_form.cleaned_data['first_name']
        user.last_name = user_form.cleaned_data['last_name']
        user.email = user_form.cleaned_data['email']
        user.phone_number = user_form.cleaned_data['phone_number']
        pic = user_form.cleaned_data.get('profile_picture')
        if pic:
            user.profile_picture = pic
        user.save()
        form.save()
        messages.success(self.request, "Student profile updated successfully.")
        return redirect(self.get_success_url())


class StudentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = StudentProfile
    template_name = 'people/confirm_delete.html'
    success_url = reverse_lazy('people:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Student'
        context['name'] = self.object.user.get_full_name() or self.object.user.username
        context['back_url'] = reverse_lazy('people:student_detail', kwargs={'pk': self.object.pk})
        return context

    def form_valid(self, form):
        user = self.object.user
        response = super().form_valid(form)
        user.delete()
        messages.success(self.request, "Student and associated account permanently deleted.")
        return response
