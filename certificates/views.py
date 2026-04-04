from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Certificate
from .forms import CertificateForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

class GenericDeleteMixin:
    template_name = 'shared/confirm_delete.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Delete Certificate'
        ctx['name'] = str(self.object)
        ctx['back_url'] = self.success_url
        return ctx

class CertificateListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Certificate
    template_name = 'certificates/certificate_list.html'
    context_object_name = 'certificates'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Document & Certificate Management'
        return ctx

class CertificateCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Certificate
    form_class = CertificateForm
    template_name = 'certificates/generic_form.html'
    success_url = reverse_lazy('certificates:certificate_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Mint Official Certificate'
        ctx['back_url'] = reverse_lazy('certificates:certificate_list')
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Certificate generated.")
        return super().form_valid(form)

class CertificateUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Certificate
    form_class = CertificateForm
    template_name = 'certificates/generic_form.html'
    success_url = reverse_lazy('certificates:certificate_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Certificate'
        ctx['back_url'] = reverse_lazy('certificates:certificate_list')
        return ctx

class CertificateDeleteView(LoginRequiredMixin, AdminRequiredMixin, GenericDeleteMixin, DeleteView):
    model = Certificate
    success_url = reverse_lazy('certificates:certificate_list')
