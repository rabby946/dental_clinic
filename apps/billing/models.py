from django.db import models
from apps.core.models import Appointment
from decimal import Decimal

def calculate_due(appointment):
    charges = Payment.objects.filter(
        appointment=appointment,
        type='charge'
    ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

    paid = Payment.objects.filter(
        appointment=appointment,
        type='paid'
    ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

    return charges - paid

class Payment(models.Model):

    TRANSACTION_TYPE = [
        ('charge', 'Charge'),
        ('paid', 'Paid'),
    ]

    PAYMENT_METHOD = [
        ('cash', 'Cash'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('card', 'Card'),
        ('online', 'Online Transfer'),
        ('onhand', 'On Hand'),
    ]

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE
    )

    method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD,
        blank=True,
        null=True
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    transaction_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.upper()} - {self.amount}"
