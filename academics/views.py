from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import AcademicSession, ClassLevel, Section, Subject
from .forms import AcademicSessionForm, ClassLevelForm, SectionForm, SubjectForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

# --- Academic Session ---
class SessionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = AcademicSession
    template_name = 'academics/session_list.html'
    context_object_name = 'sessions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Academic Sessions'
        return context

class SessionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:session_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Academic Session'
        context['back_url'] = reverse_lazy('academics:session_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Academic Session created successfully.")
        return super().form_valid(form)

# --- Class Levels ---
class ClassListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ClassLevel
    template_name = 'academics/class_list.html'
    context_object_name = 'classes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Class Levels'
        return context

class ClassCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ClassLevel
    form_class = ClassLevelForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:class_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Class Level'
        context['back_url'] = reverse_lazy('academics:class_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Class Level created successfully.")
        return super().form_valid(form)

# --- Sections ---
class SectionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Section
    template_name = 'academics/section_list.html'
    context_object_name = 'sections'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sections'
        return context

class SectionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:section_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Section'
        context['back_url'] = reverse_lazy('academics:section_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Section created successfully.")
        return super().form_valid(form)

# --- Subjects ---
class SubjectListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Subject
    template_name = 'academics/subject_list.html'
    context_object_name = 'subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Subjects'
        return context

class SubjectCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:subject_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Subject'
        context['back_url'] = reverse_lazy('academics:subject_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Subject created successfully.")
        return super().form_valid(form)
