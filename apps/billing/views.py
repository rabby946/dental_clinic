from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from apps.core.models import Appointment
from .models import Payment
from apps.patients.views import patient_required
from apps.doctors.decorators import doctor_required
from apps.billing.models import calculate_due

@patient_required
def patient_pay_init(request, appointment_id):
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

@doctor_required
def add_charge(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))

        Payment.objects.create(
            appointment=appointment,
            type='charge',
            amount=amount
        )

        messages.success(request, "Charge added successfully.")
        return redirect('doctors:appointment_detail', pk=appointment.id)

    return render(request, 'billing/add_charge.html', {
        'appointment': appointment
    })

@doctor_required
def add_manual_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        method = request.POST.get('method')

        Payment.objects.create(
            appointment=appointment,
            type='paid',
            method=method,
            amount=amount
        )

        messages.success(request, "Payment recorded.")
        return redirect('doctors:appointment_detail', pk=appointment.id)

    return render(request, 'billing/add_manual_payment.html', {
        'appointment': appointment,
        'methods': Payment.PAYMENT_METHOD
    })
