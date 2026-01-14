from django.contrib import admin
from .models import Prescription, PrescriptionItem

# Inline for Prescription Items
class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1
    autocomplete_fields = ['medicine']
    fields = [
        'medicine', 'dose', 'frequency', 'duration_value', 'duration_unit', 'timing', 'instructions'
    ]

# Inline for Prescription inside Appointment
class PrescriptionInline(admin.StackedInline):
    model = Prescription
    can_delete = False
    extra = 0
    show_change_link = True  # Links to full Prescription if needed
    inlines = [PrescriptionItemInline]

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'patient_name', 'created_at']
    search_fields = ['appointment__patient__name', 'appointment__id']
    list_filter = ['created_at']
    inlines = [PrescriptionItemInline]

    def patient_name(self, obj):
        return obj.appointment.patient.name
    patient_name.short_description = 'Patient'
