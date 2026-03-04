from django.db import models
from apps.core.models import Appointment
from apps.medicines.models import Medicine

from django.db import models
from apps.core.models import Appointment


class Prescription(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )

    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription #{self.id} - Appt {self.appointment.id}"

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.medicine.name}"
