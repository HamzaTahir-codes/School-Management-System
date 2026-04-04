from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import AcademicSession, ClassLevel, Section, Subject, TeacherAssignment
from .forms import AcademicSessionForm, ClassLevelForm, SectionForm, SubjectForm, TeacherAssignmentForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

# ===================== SESSIONS =====================
class SessionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = AcademicSession
    template_name = 'academics/session_list.html'
    context_object_name = 'sessions'

class SessionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:session_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Create Academic Session'
        ctx['back_url'] = reverse_lazy('academics:session_list')
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Academic session created.")
        return super().form_valid(form)

class SessionUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:session_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Academic Session'
        ctx['back_url'] = reverse_lazy('academics:session_list')
        return ctx

class SessionDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = AcademicSession
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('academics:session_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Delete Session'
        ctx['name'] = str(self.object)
        ctx['back_url'] = reverse_lazy('academics:session_list')
        return ctx

# ===================== CLASS LEVELS =====================
class ClassListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ClassLevel
    template_name = 'academics/class_list.html'
    context_object_name = 'classes'

class ClassCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ClassLevel
    form_class = ClassLevelForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:class_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Class Level'
        ctx['back_url'] = reverse_lazy('academics:class_list')
        return ctx

class ClassUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ClassLevel
    form_class = ClassLevelForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:class_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Class Level'
        ctx['back_url'] = reverse_lazy('academics:class_list')
        return ctx

class ClassDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = ClassLevel
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('academics:class_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Delete Class Level'
        ctx['name'] = str(self.object)
        ctx['back_url'] = reverse_lazy('academics:class_list')
        return ctx

# ===================== SECTIONS =====================
class SectionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Section
    template_name = 'academics/section_list.html'
    context_object_name = 'sections'

class SectionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:section_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Section'
        ctx['back_url'] = reverse_lazy('academics:section_list')
        return ctx

class SectionUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:section_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Section'
        ctx['back_url'] = reverse_lazy('academics:section_list')
        return ctx

class SectionDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Section
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('academics:section_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Delete Section'
        ctx['name'] = str(self.object)
        ctx['back_url'] = reverse_lazy('academics:section_list')
        return ctx

# ===================== SUBJECTS =====================
class SubjectListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Subject
    template_name = 'academics/subject_list.html'
    context_object_name = 'subjects'

class SubjectCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:subject_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Subject'
        ctx['back_url'] = reverse_lazy('academics:subject_list')
        return ctx

class SubjectUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:subject_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Subject'
        ctx['back_url'] = reverse_lazy('academics:subject_list')
        return ctx

class SubjectDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Subject
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('academics:subject_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Delete Subject'
        ctx['name'] = str(self.object)
        ctx['back_url'] = reverse_lazy('academics:subject_list')
        return ctx

# ===================== TEACHER ASSIGNMENTS =====================
class AssignmentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = TeacherAssignment
    template_name = 'academics/assignment_list.html'
    context_object_name = 'assignments'
    def get_queryset(self):
        return TeacherAssignment.objects.select_related('teacher__user', 'class_level', 'section', 'subject', 'academic_session').all()

class AssignmentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = TeacherAssignment
    form_class = TeacherAssignmentForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:assignment_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Assign Teacher to Class'
        ctx['back_url'] = reverse_lazy('academics:assignment_list')
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Teacher assignment configured.")
        return super().form_valid(form)

class AssignmentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = TeacherAssignment
    form_class = TeacherAssignmentForm
    template_name = 'academics/generic_form.html'
    success_url = reverse_lazy('academics:assignment_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Assignment'
        ctx['back_url'] = reverse_lazy('academics:assignment_list')
        return ctx

class AssignmentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = TeacherAssignment
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('academics:assignment_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Remove Assignment'
        ctx['name'] = str(self.object)
        ctx['back_url'] = reverse_lazy('academics:assignment_list')
        return ctx
