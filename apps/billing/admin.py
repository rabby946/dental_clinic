from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'amount', 'status', 'created_at']
    search_fields = ['appointment__patient__name', 'appointment__id']
    list_filter = ['status', 'created_at']
