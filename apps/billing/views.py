from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Max
from django.utils import timezone
from apps.core.models import Appointment
from apps.patients.models import Patient
from .models import Payment, calculate_due
from apps.core.models import Appointment
from .models import Payment
from apps.patients.views import patient_required
from apps.doctors.decorators import doctor_required
from apps.billing.models import calculate_due

@patient_required
def patient_init(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient__user=request.user
    )

    due_amount = calculate_due(appointment)

    if due_amount <= 0:
        messages.info(request, "No due payment.")
        return redirect('patients:payment_list')

    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', '0'))

        if amount <= 0 or amount > due_amount:
            messages.error(request, "Invalid payment amount.")
            return redirect(request.path)

        # 🔥 এখানে bKash payment initiation code যাবে
        # bkash_create_payment(amount, appointment.id)

        return redirect('billing:bkash_callback')

    return render(request, 'billing/patient_pay.html', {
        'appointment': appointment,
        'due_amount': due_amount
    })

@csrf_exempt
def bkash_callback(request):
    """
    bKash successful payment hit করবে এখানে
    """

    # 🔥 Real implementation এ bkash payload verify করবে
    appointment_id = request.POST.get('appointment_id')
    amount = Decimal(request.POST.get('amount'))
    trx_id = request.POST.get('trx_id')

    appointment = get_object_or_404(Appointment, id=appointment_id)

    Payment.objects.create(
        appointment=appointment,
        type='paid',
        method='bkash',
        amount=amount,
        transaction_id=trx_id
    )

    messages.success(request, "Payment successful!")
    return redirect('patients:payment_list')


@login_required
@require_http_methods(["GET", "POST"])
def patient_billing(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    # 🔹 Get latest appointment
    appointment = Appointment.objects.filter(
        patient=patient
    ).order_by('-created_at').first()
    

    today = timezone.now().date()
    # 🔹 If no appointment exists → create one
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

    # ================= POST =================
    if request.method == "POST":
        try:
            amount = Decimal(request.POST.get("amount"))
            payment_type = request.POST.get("type")
            method = request.POST.get("method")

            if amount <= 0:
                return JsonResponse({"error": "Invalid amount"}, status=400)

            Payment.objects.create(
                appointment=appointment,
                type=payment_type,
                method=method if payment_type == "paid" else None,
                amount=amount
            )

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    # ================= GET =================
    payments = Payment.objects.filter(
        appointment__patient=patient
    ).order_by('-created_at')[:100]

    due = calculate_due(appointment)

    return render(request, "billing/appointment_billing.html", {
        "patient": patient,
        "appointment": appointment,
        "payments": payments,
        "due": due
    })