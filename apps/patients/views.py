# apps/patients/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from apps.core.models import Appointment
from apps.prescriptions.models import Prescription
from apps.billing.models import Payment
from django.contrib.auth.models import User

# -------------------
# Decorator / Mixin
# -------------------
def patient_required(view_func):
    """Decorator to allow only Patient group users"""
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Patient').exists():
            return view_func(request, *args, **kwargs)
        messages.error(request, "You must be logged in as a Patient to access this page.")
        return redirect('/')
    return wrapper

class PatientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Patient').exists()

# Login / Logout
def patient_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        try:
            patient_user = User.objects.get(username=phone)
        except User.DoesNotExist:
            messages.error(request, "Patient user not found.")
            return redirect('/login/')  # patient login page

        # Authenticate using username + password
        user = authenticate(request, username=patient_user.username, password=password)

        if user is not None and user.groups.filter(name='Patient').exists():
            login(request, user)
            messages.success(request, f"Welcome {user.get_full_name() or user.username}!")
            return redirect('/patients/dashboard/')  # patient dashboard
        else:
            messages.error(request, "ফোন নাম্বার বা পাসওয়ার্ড ভুল।")
            return redirect('/login/')  # patient login page

    # GET request: render login form
    return render(request, 'patients/login.html')

def patient_logout(request):
    logout(request)
    messages.info(request, "আপনি লগআউট হয়েছেন।")
    return redirect('/')

# -------------------
# Dashboard
# -------------------
@patient_required
def patient_dashboard(request):
    appointments = Appointment.objects.filter(patient__user=request.user).order_by('-date')
    prescriptions = Prescription.objects.filter(appointment__patient__user=request.user).order_by('-created_at')
    payments = Payment.objects.filter(patient__user=request.user).order_by('-created_at')
    return render(request, 'patients/dashboard.html', {
        'appointments': appointments,
        'prescriptions': prescriptions,
        'payments': payments,
    })

# -------------------
# Profile
# -------------------
@patient_required
def patient_profile_update(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        # update user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('patients:dashboard')

    # GET request, show current user info
    context = {
        'user': user
    }
    return render(request, 'patients/profile.html', context)

# -------------------
# Prescriptions
# -------------------
@patient_required
def prescription_list(request):
    prescriptions = Prescription.objects.filter(appointment__patient__user=request.user).order_by('-created_at')
    return render(request, 'patients/prescription_list.html', {'prescriptions': prescriptions})

@patient_required
def prescription_detail(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, appointment__patient__user=request.user)
    return render(request, 'patients/prescription_detail.html', {'prescription': prescription})

# -------------------
# Payments
# -------------------
@patient_required
def payment_list(request):
    payments = Payment.objects.filter(patient__user=request.user).order_by('-created_at')
    return render(request, 'patients/payment_list.html', {'payments': payments})

@patient_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk, patient__user=request.user)
    return render(request, 'patients/payment_detail.html', {'payment': payment})

# -------------------
# Appointments
# -------------------
@patient_required
def appointment_list(request):
    appointments = Appointment.objects.filter(patient__user=request.user).order_by('-date', 'time')
    return render(request, 'patients/appointments.html', {'appointments': appointments})

@patient_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient__user=request.user)
    return render(request, 'patients/appointment_detail.html', {'appointment': appointment})
