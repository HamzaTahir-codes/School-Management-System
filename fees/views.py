from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import FeeStructure, StudentFeePayment
from .forms import FeeStructureForm, StudentFeePaymentForm

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

# --- Fee Structures ---
class FeeStructureListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = FeeStructure
    template_name = 'fees/fee_structure_list.html'
    context_object_name = 'structures'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Fee Structures'
        return ctx

class FeeStructureCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = FeeStructure
    form_class = FeeStructureForm
    template_name = 'fees/generic_form.html'
    success_url = reverse_lazy('fees:fee_structure_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Define Fee Structure'
        ctx['back_url'] = reverse_lazy('fees:fee_structure_list')
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Fee structure created.")
        return super().form_valid(form)

class FeeStructureUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = FeeStructure
    form_class = FeeStructureForm
    template_name = 'fees/generic_form.html'
    success_url = reverse_lazy('fees:fee_structure_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Fee Structure'
        ctx['back_url'] = reverse_lazy('fees:fee_structure_list')
        return ctx

class FeeStructureDeleteView(LoginRequiredMixin, AdminRequiredMixin, GenericDeleteMixin, DeleteView):
    model = FeeStructure
    success_url = reverse_lazy('fees:fee_structure_list')

# --- Student Payments ---
class StudentFeePaymentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = StudentFeePayment
    template_name = 'fees/payment_list.html'
    context_object_name = 'payments'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Student Payments'
        return ctx

class StudentFeePaymentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = StudentFeePayment
    form_class = StudentFeePaymentForm
    template_name = 'fees/generic_form.html'
    success_url = reverse_lazy('fees:payment_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Record Payment'
        ctx['back_url'] = reverse_lazy('fees:payment_list')
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Payment recorded.")
        return super().form_valid(form)

class StudentFeePaymentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = StudentFeePayment
    form_class = StudentFeePaymentForm
    template_name = 'fees/generic_form.html'
    success_url = reverse_lazy('fees:payment_list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Payment'
        ctx['back_url'] = reverse_lazy('fees:payment_list')
        return ctx

class StudentFeePaymentDeleteView(LoginRequiredMixin, AdminRequiredMixin, GenericDeleteMixin, DeleteView):
    model = StudentFeePayment
    success_url = reverse_lazy('fees:payment_list')
