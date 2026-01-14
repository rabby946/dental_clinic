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
# apps/doctors/views.py
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def doctor_login(request):
    """
    Doctor login view
    GET: render login form (or redirect to dashboard if already logged in)
    POST: authenticate and login doctor
    """

    # If already logged in, redirect to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/doctors/dashboard/')

    if request.method == 'POST':
        password = request.POST.get('password')

        try:
            # Doctor user ID 1
            doctor_user = User.objects.get(id=1)
        except User.DoesNotExist:
            messages.error(request, "Doctor user not found.")
            return redirect('/doctors/login/')

        # Authenticate using doctor username + submitted password
        user = authenticate(request, username=doctor_user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome Dr. {user.get_full_name() or user.username}!")
            return redirect('/doctors/dashboard/')  # doctor dashboard
        else:
            messages.error(request, "Invalid password.")
            return redirect('/doctors/login/')

    # GET request: show login form
    return render(request, 'doctors/login.html')


from django.contrib.auth.views import LogoutView

def doctor_logout(request):
    """
    Doctor logout view
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('/doctors/login/')
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
