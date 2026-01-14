from django.contrib import admin
from .models import Appointment, Document
from apps.prescriptions.admin import PrescriptionInline  # import the inline

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient_name', 'date', 'time', 'problem', 'status', 'created_at']
    search_fields = ['patient__name', 'problem']
    list_filter = ['status', 'date']
    ordering = ['-date', 'time']
    inlines = [PrescriptionInline]  # <-- add this

    def patient_name(self, obj):
        return obj.patient.name
    patient_name.short_description = 'Patient'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'patient_name', 'file', 'uploaded_at']
    search_fields = ['title', 'patient__name']
    list_filter = ['uploaded_at']
    ordering = ['-uploaded_at']

    def patient_name(self, obj):
        return obj.patient.name
    patient_name.short_description = 'Patient'
