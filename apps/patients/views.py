from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from apps.core.models import Appointment
from apps.prescriptions.models import Prescription
from apps.billing.models import Payment
from django.contrib.auth.models import User

# Decorator for patient-only access
class PatientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Patient').exists()

# Login / Logout
class PatientLoginView(LoginView):
    template_name = 'patients/login.html'

class PatientLogoutView(LogoutView):
    next_page = reverse_lazy('patients:login')

# Dashboard
class PatientDashboardView(LoginRequiredMixin, PatientRequiredMixin, TemplateView):
    template_name = 'patients/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(patient__user=self.request.user).order_by('-date')
        context['prescriptions'] = Prescription.objects.filter(appointment__patient__user=self.request.user).order_by('-created_at')
        context['payments'] = Payment.objects.filter(patient__user=self.request.user).order_by('-created_at')
        return context

# Profile
class PatientProfileUpdateView(LoginRequiredMixin, PatientRequiredMixin, UpdateView):
    template_name = 'patients/profile.html'
    model = User
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('patients:dashboard')

    def get_object(self, queryset=None):
        return self.request.user

# Prescription List
class PrescriptionListView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    template_name = 'patients/prescription_list.html'
    model = Prescription

    def get_queryset(self):
        return Prescription.objects.filter(appointment__patient__user=self.request.user).order_by('-created_at')

# Prescription Detail
class PrescriptionDetailView(LoginRequiredMixin, PatientRequiredMixin, DetailView):
    template_name = 'patients/prescription_detail.html'
    model = Prescription

    def get_queryset(self):
        return Prescription.objects.filter(appointment__patient__user=self.request.user)

# Payments
class PaymentListView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    template_name = 'patients/payment_list.html'
    model = Payment

    def get_queryset(self):
        return Payment.objects.filter(patient__user=self.request.user).order_by('-created_at')

class PaymentDetailView(LoginRequiredMixin, PatientRequiredMixin, DetailView):
    template_name = 'patients/payment_detail.html'
    model = Payment

    def get_queryset(self):
        return Payment.objects.filter(patient__user=self.request.user)
