from django.db import models
from apps.core.models import Appointment

class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('card', 'Card'),
        ('online', 'Online Transfer'),
        ('onhand', 'On Hand')
    ]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    type = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    status = models.CharField(max_length=20, default='paid')
    transaction_id = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.method}"
