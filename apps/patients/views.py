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

from django.db.models import Sum
from django.utils.timezone import now
from apps.core.models import Appointment
from apps.prescriptions.models import Prescription
from apps.billing.models import Payment

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import render, redirect

from django.db.models import Sum
from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from apps.core.models import Document

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

# Dashboard

from django.db.models import Sum
from django.utils.timezone import now

@patient_required
def patient_dashboard(request):
    patient = request.user.patient
    today = now().date()

    # -------------------
    # Appointments
    # -------------------
    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('-date')

    upcoming_appointments = appointments.filter(date__gte=today)
    completed_appointments = appointments.filter(status='completed')

    # -------------------
    # Prescriptions
    # -------------------
    prescriptions = Prescription.objects.filter(
        appointment__patient=patient
    ).order_by('-created_at')

    # -------------------
    # Payments (Ledger based)
    # -------------------
    payments = Payment.objects.filter(
        appointment__patient=patient
    )

    total_charge = payments.filter(type='charge').aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_paid = payments.filter(type='paid').aggregate(
        total=Sum('amount')
    )['total'] or 0

    due_amount = total_charge - total_paid

    context = {
        'patient': patient,

        # analytics
        'total_appointments': appointments.count(),
        'upcoming_count': upcoming_appointments.count(),
        'completed_count': completed_appointments.count(),

        'total_charge': total_charge,
        'total_paid': total_paid,
        'due_amount': due_amount,

        # recent items
        'appointments': appointments[:5],
        'prescriptions': prescriptions[:5],
        'payments': payments.order_by('-created_at')[:5],
    }

    return render(request, 'patients/dashboard.html', context)


# -------------------
# Profile
# -------------------

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@patient_required
def patient_profile_update(request):
    user = request.user

    try:
        patient = user.patient
    except:
        messages.error(request, "Patient profile not found.")
        return redirect('patients:dashboard')

    if request.method == 'POST':
        # User fields
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        # Patient fields
        address = request.POST.get('address', '').strip()
        blood_group = request.POST.get('blood_group', '').strip()

        # Update User
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        patient.name = first_name + last_name
        user.save()

        # Update Patient
        patient.address = address
        patient.blood_group = blood_group
        patient.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('patients:profile')

    context = {
        'user': user,
        'patient': patient,
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
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas

@patient_required
def prescription_download(request, pk):
    prescription = get_object_or_404(
        Prescription,
        pk=pk,
        appointment__patient__user=request.user
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prescription_{pk}.pdf"'

    p = canvas.Canvas(response)
    y = 800

    patient = prescription.appointment.patient

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Medical Prescription")
    y -= 40

    p.setFont("Helvetica", 10)
    p.drawString(50, y, f"Patient: {patient.name}")
    y -= 15
    p.drawString(50, y, f"Date: {prescription.created_at.date()}")
    y -= 30

    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Medicines:")
    y -= 20

    p.setFont("Helvetica", 10)
    for item in prescription.items.all():
        p.drawString(
            50, y,
            f"- {item.medicine.name} | {item.dosage} | {item.duration}"
        )
        y -= 15
        if item.instructions:
            p.drawString(70, y, f"Instruction: {item.instructions}")
            y -= 15

    if prescription.note:
        y -= 20
        p.setFont("Helvetica-Bold", 11)
        p.drawString(50, y, "Doctor's Note:")
        y -= 15
        p.setFont("Helvetica", 10)
        p.drawString(50, y, prescription.note)

    p.showPage()
    p.save()

    return response





@patient_required
def payment_list(request):
    payments = Payment.objects.filter(appointment__patient__user=request.user).order_by('-created_at')
    total_charge = payments.filter(type='charge').aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_paid = payments.filter(type='paid').aggregate(total=Sum('amount'))['total'] or Decimal('0')
    due_amount = total_charge - total_paid

    context = {
        'payments': payments,
        'due_amount': due_amount,
        # assume last active appointment
        'appointment_id': payments.first().appointment.id if payments else None
    }

    return render(request, 'patients/payment_list.html', context)



@patient_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment,pk=pk,appointment__patient__user=request.user)
    return render(request, 'patients/payment_detail.html', {'payment': payment})


# Appointments
@patient_required
def appointment_list(request):
    appointments = Appointment.objects.filter(patient__user=request.user).order_by('-date', 'time')
    return render(request, 'patients/appointments.html', {'appointments': appointments})

@patient_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient__user=request.user)
    return render(request, 'patients/appointment_detail.html', {'appointment': appointment})



@patient_required
def change_password(request):
    user = request.user

    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        if not check_password(old_password, user.password):
            messages.error(request, "বর্তমান পাসওয়ার্ড সঠিক নয়।")
            return redirect('patients:change_password')
        if new_password != confirm_password:
            messages.error(request, "নতুন পাসওয়ার্ড মিলছে না।")
            return redirect('patients:change_password')
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "পাসওয়ার্ড সফলভাবে পরিবর্তন হয়েছে।")
        return redirect('patients:dashboard')
    return render(request, 'patients/change_password.html')


# -------------------
# Documents
# -------------------

@patient_required
def documents(request):
    patient = request.user.patient
    documents = (Document.objects.filter(patient=patient).order_by('-uploaded_at'))
    return render(request, 'patients/documents.html', {
        'documents': documents
    })


@patient_required
def document_details(request, pk):
    patient = request.user.patient
    document = get_object_or_404(Document,pk=pk,patient=patient)
    return render(request, 'patients/document_details.html', {
        'document': document
    })
