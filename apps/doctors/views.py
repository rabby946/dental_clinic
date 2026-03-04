# apps/doctors/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.utils import timezone
from apps.core.models import Appointment
from apps.patients.models import Patient
from apps.doctors.decorators import doctor_required
from apps.utils import upload_to_cloud
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from apps.doctors.decorators import doctor_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from apps.patients.models import Patient
from apps.core.models import Appointment, Document
from apps.prescriptions.models import Prescription

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def doctor_login(request):

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
    today = timezone.now().date()

    # 1️⃣ Completed today
    completed_today = Appointment.objects.filter(
        date=today,
        status='completed'
    ).count()

    # 2️⃣ Total patients
    total_patients = Patient.objects.count()
    appointments_today = Appointment.objects.filter(date=timezone.now().date()).order_by('time')
    pending_appointments = Appointment.objects.filter(status='pending').order_by('date', 'time')
    return render(request, 'doctors/dashboard.html', {
        'appointments_today': appointments_today,
        'pending_appointments': pending_appointments,
        'completed_today': completed_today,
        'total_patients': total_patients,
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
    patients = Patient.objects.all().order_by('-created_at')

    context = {
        "patients": patients
    }

    return render(request, "doctors/patient_list.html", context)

@doctor_required
def patient_search(request):
    if request.method == 'POST':
        phone = request.POST.get('phone').strip()

        if not phone:
            messages.error(request, "Phone number required.")
            return redirect('doctors:doctor_dashboard')

        try:
            patient = Patient.objects.get(phone=phone)
            return redirect('doctors:patient_detail', pk=patient.id)

        except Patient.DoesNotExist:
            request.session['new_patient_phone'] = phone
            return redirect('doctors:patient_confirm_create')

    return redirect('doctors:doctor_dashboard')

@doctor_required
def patient_confirm_create(request):
    phone = request.session.get('new_patient_phone')

    if not phone:
        return redirect('doctors:doctor_dashboard')

    return render(request, 'doctors/patient_confirm_create.html', {
        'phone': phone
    })

@doctor_required
def patient_create(request):
    phone = request.session.get('new_patient_phone')

    if not phone:
        return redirect('doctors:doctor_dashboard')

    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        dob = request.POST.get('b_date')

        patient = Patient.objects.create(
            name=name,
            phone=phone,
            gender=gender,
            date_of_birth=dob,
        )

        del request.session['new_patient_phone']

        messages.success(request, "Patient created successfully.")
        return redirect('doctors:patient_detail', pk=patient.id)

    return render(request, 'doctors/patient_create.html', {'phone': phone})

@doctor_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    appointments = patient.appointments.order_by('-date')
    prescriptions = Prescription.objects.filter(
        appointment__patient=patient
    ).order_by('-created_at')

    documents = Document.objects.filter(patient=patient).order_by('-uploaded_at')
    
    age=None

    if patient.date_of_birth:
        today = timezone.now().date()
        age = today.year - patient.date_of_birth.year - (
            (today.month, today.day) <
            (patient.date_of_birth.month, patient.date_of_birth.day)
        )
    context = {
        'patient': patient,
        'appointments': appointments,
        'prescriptions': prescriptions,
        'documents': documents,
        'age' : age,
    }
    return render(request, 'doctors/patient_detail.html', context)



@doctor_required
def add_document(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')

        if not title or not file:
            messages.error(request, "Title and file are required.")
            return redirect('doctors:add_document', patient_id=patient.id)

        Document.objects.create(
            patient=patient,
            title=title,
            file=file
        )

        messages.success(request, "Document uploaded successfully.")
        return redirect('doctors:patient_detail', pk=patient.id)

    return render(request, 'doctors/add_document.html', {
        'patient': patient
    })


@login_required
def document_detail(request, pk):
    document = get_object_or_404(
        Document.objects.select_related('patient'),
        pk=pk
    )

    return render(request, "doctors/document_detail.html", {
        "document": document
    })