from django.db import models
from apps.core.models import Appointment
from apps.medicines.models import Medicine

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription #{self.id}"

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.medicine.name}"
