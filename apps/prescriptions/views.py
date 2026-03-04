from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Max
from django.utils import timezone
from apps.patients.models import Patient
from apps.core.models import Appointment
from apps.prescriptions.models import Prescription, PrescriptionItem
from apps.medicines.models import Medicine

@login_required
def prescription_create(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    appointment = (
        Appointment.objects
        .filter(patient=patient)
        .order_by('-date', '-time')
        .first()
    )
    

    today = timezone.now().date()
    if not appointment:
    # Get today's last serial
        last_serial = (
            Appointment.objects
            .filter(date=today)
            .aggregate(Max('serial_number'))['serial_number__max']
        )

        next_serial = (last_serial or 0) + 1

        appointment = Appointment.objects.create(
            patient=patient,
            date=today,
            time=timezone.now().time(),
            serial_number=next_serial,
            problem="Consultation",
            status='completed'
        )

    if request.method == 'POST':
        note = request.POST.get('note', '')

        prescription = Prescription.objects.create(
            appointment=appointment,
            note=note
        )

        medicine_ids = request.POST.getlist('medicine')
        dosages = request.POST.getlist('dosage')
        durations = request.POST.getlist('duration')
        instructions = request.POST.getlist('instructions')

        for medicine_id, dosage, duration, instruction in zip(
            medicine_ids, dosages, durations, instructions
        ):
            if medicine_id:  # ignore empty rows
                PrescriptionItem.objects.create(
                    prescription=prescription,
                    medicine_id=medicine_id,
                    dosage=dosage,
                    duration=duration,
                    instructions=instruction,
                )

        return redirect('doctors:patient_detail', pk=patient.id)

    medicines = Medicine.objects.all()

    return render(request, 'prescriptions/create.html', {
        'patient': patient,
        'medicines': medicines,
    })

# patients/models.py


@login_required
def prescription_detail(request, pk):
    prescription = get_object_or_404(
        Prescription.objects.select_related(
            "appointment__patient"
        ).prefetch_related(
            "items__medicine"
        ),
        pk=pk
    )
    age=None

    if prescription.appointment.patient.date_of_birth:
        today = timezone.now().date()
        age = today.year - prescription.appointment.patient.date_of_birth.year - (
            (today.month, today.day) <
            (prescription.appointment.patient.date_of_birth.month, prescription.appointment.patient.date_of_birth.day)
        )
    return render(request, "prescriptions/detail.html", {
        "prescription": prescription,
        "age" : age,
    })
