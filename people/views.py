from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
import random
import string

from accounts.models import User
from .models import TeacherProfile, ParentProfile, StudentProfile
from .forms import TeacherCreationForm, ParentCreationForm, StudentCreationForm

def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

class BaseProfileCreateView(LoginRequiredMixin, CreateView):
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
            # Future enhancement: Message admin the generated password or email the user
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
        return super().form_valid(form)

class TeacherListView(LoginRequiredMixin, ListView):
    model = TeacherProfile
    template_name = 'people/teacher_list.html'
    context_object_name = 'teachers'

class TeacherCreateView(BaseProfileCreateView):
    model = TeacherProfile
    form_class = TeacherCreationForm
    template_name = 'people/teacher_form.html'
    success_url = reverse_lazy('people:teacher_list')
    role = User.Role.TEACHER

class ParentListView(LoginRequiredMixin, ListView):
    model = ParentProfile
    template_name = 'people/parent_list.html'
    context_object_name = 'parents'

class ParentCreateView(BaseProfileCreateView):
    model = ParentProfile
    form_class = ParentCreationForm
    template_name = 'people/parent_form.html'
    success_url = reverse_lazy('people:parent_list')
    role = User.Role.PARENT

class StudentListView(LoginRequiredMixin, ListView):
    model = StudentProfile
    template_name = 'people/student_list.html'
    context_object_name = 'students'

class StudentCreateView(BaseProfileCreateView):
    model = StudentProfile
    form_class = StudentCreationForm
    template_name = 'people/student_form.html'
    success_url = reverse_lazy('people:student_list')
    role = User.Role.STUDENT
