from twilio.rest import Client
from django.conf import settings

def send_whatsapp(phone, message):
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

    client.messages.create(
        from_=settings.TWILIO_WHATSAPP_FROM,
        body=message,
        to=f"whatsapp:+88{phone}"  # Bangladesh
    )
