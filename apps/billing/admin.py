from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'appointment',
        'type',
        'amount',
        'method',
        'created_at',
    )

    list_filter = (
        'type',
        'method',
    )

    search_fields = (
        'appointment__patient__name',
        'appointment__patient__phone',
        'transaction_id',
    )

    ordering = ('-created_at',)
