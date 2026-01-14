# apps/doctors/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.utils import timezone
from apps.core.models import Appointment
from apps.patients.models import Patient
from apps.doctors.decorators import doctor_required

# -------------------
# Login / Logout
# -------------------
# apps/doctors/views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from apps.doctors.decorators import doctor_required
from django.utils.decorators import method_decorator

# -------------------
# Login / Logout
# -------------------
class DoctorLoginView(LoginView):
    template_name = 'doctors/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is in Doctor group
            if user.groups.filter(name='Doctor').exists():
                login(request, user)  # log in the doctor
                messages.success(request, f"Welcome Dr. {user.get_full_name() or user.username}!")
                return redirect(reverse('doctor_dashboard'))
            else:
                messages.error(request, "You are not authorized as a Doctor.")
                return redirect(reverse('doctor_login'))
        else:
            messages.error(request, "Invalid username or password.")
            return redirect(reverse('doctor_login'))

class DoctorLogoutView(LogoutView):
    next_page = '/doctors/login/'  # redirect to login
    def dispatch(self, request, *args, **kwargs):
        logout(request)  # remove login and decorator access
        return super().dispatch(request, *args, **kwargs)


# -------------------
# Dashboard
# -------------------
@doctor_required
def doctor_dashboard(request):
    appointments_today = Appointment.objects.filter(date=timezone.now().date()).order_by('time')
    pending_appointments = Appointment.objects.filter(status='pending').order_by('date', 'time')
    return render(request, 'doctors/dashboard.html', {
        'appointments_today': appointments_today,
        'pending_appointments': pending_appointments,
    })

# -------------------
# Appointments
# -------------------
@doctor_required
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-date', 'time')
    return render(request, 'doctors/appointments.html', {'appointments': appointments})

@doctor_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'doctors/appointment_detail.html', {'appointment': appointment})

# -------------------
# Patients
# -------------------
@doctor_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'doctors/patients.html', {'patients': patients})

@doctor_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'doctors/patient_detail.html', {'patient': patient})
