from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Mark, FinalReport
from .forms import MarkForm, FinalReportForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

class GenericDeleteMixin:
    template_name = 'shared/confirm_delete.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Delete {self.model.__name__}'
        ctx['name'] = str(self.object)
        ctx['back_url'] = self.success_url
        return ctx

# --- Marks ---
class MarkListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Mark
    template_name = 'grading/mark_list.html'
    context_object_name = 'marks'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Student Term Marks'
        return ctx

class MarkCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Mark
    form_class = MarkForm
    template_name = 'grading/generic_form.html'
    success_url = reverse_lazy('grading:mark_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Record Subject Marks'
        ctx['back_url'] = reverse_lazy('grading:mark_list')
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Marks recorded.")
        return super().form_valid(form)

class MarkUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Mark
    form_class = MarkForm
    template_name = 'grading/generic_form.html'
    success_url = reverse_lazy('grading:mark_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Marks'
        ctx['back_url'] = reverse_lazy('grading:mark_list')
        return ctx

class MarkDeleteView(LoginRequiredMixin, AdminRequiredMixin, GenericDeleteMixin, DeleteView):
    model = Mark
    success_url = reverse_lazy('grading:mark_list')

# --- Final Reports ---
class FinalReportListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = FinalReport
    template_name = 'grading/final_report_list.html'
    context_object_name = 'reports'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Final Aggregated Reports'
        return ctx

class FinalReportCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = FinalReport
    form_class = FinalReportForm
    template_name = 'grading/generic_form.html'
    success_url = reverse_lazy('grading:report_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Generate Final Report'
        ctx['back_url'] = reverse_lazy('grading:report_list')
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Report generated.")
        return super().form_valid(form)

class FinalReportUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = FinalReport
    form_class = FinalReportForm
    template_name = 'grading/generic_form.html'
    success_url = reverse_lazy('grading:report_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Final Report'
        ctx['back_url'] = reverse_lazy('grading:report_list')
        return ctx

class FinalReportDeleteView(LoginRequiredMixin, AdminRequiredMixin, GenericDeleteMixin, DeleteView):
    model = FinalReport
    success_url = reverse_lazy('grading:report_list')
