from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests

from django.db import transaction
from apps.core.utils import get_time_by_serial
from apps.core.models import Appointment
from apps.patients.models import Patient
from datetime import datetime, time, timedelta
from apps.utils import send_whatsapp
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group





# Home page
def home(request):
    return render(request, 'core/home.html')

# Services page
def services(request):
    return render(request, 'core/services.html')

# Contact page
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        url = "https://api.brevo.com/v3/smtp/email"

        payload = {
            "sender": {
                "name": "Dental Clinic Website",
                "email": settings.BREVO_SENDER_EMAIL
            },
            "to": [
                {
                    "email": settings.ADMIN_EMAIL,
                    "name": "Admin"
                }
            ],
            "subject": f"New Contact Message from {name}",
            "htmlContent": f"""
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong></p>
                <p>{message}</p>
            """
        }
        headers = {
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 201:
            print(response.text)  # debugging
        return render(request, 'core/contact.html', {'success': True})
    return render(request, 'core/contact.html')


def appointment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        date_str = request.POST.get("date")
        problem = request.POST.get("message")
        print(name, phone, date_str, problem)
        if not all([name, phone, date_str]):
            messages.error(request, "সব তথ্য সঠিকভাবে দিন।")
            return redirect("appointment")
        appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if appointment_date.weekday() == 4:
            messages.error(request,"শুক্রবার আমাদের চেম্বার বন্ধ থাকে। অন্য তারিখ নির্বাচন করুন।")
            return redirect("appointment")

        patient_created = False
        patient = Patient.objects.filter(phone=phone).first()

        if not patient:
            user = User.objects.create_user(username=phone, password=phone)
            patient_group, _ = Group.objects.get_or_create(name="Patient")
            user.groups.add(patient_group)

            patient = Patient.objects.create(user=user, name=name, phone=phone)
            patient_created = True

        with transaction.atomic():
            todays_appointments = (Appointment.objects.select_for_update().filter(date=appointment_date))
            total_today = todays_appointments.count()
            if total_today >= 15:
                messages.error(request,"আজকের সব স্লট পূর্ণ। অনুগ্রহ করে অন্য তারিখ নির্বাচন করুন।")
                return redirect("appointment")
            serial = total_today + 1
            time = get_time_by_serial(serial)
            Appointment.objects.create(patient=patient,date=appointment_date,time=time,serial_number=serial,problem=problem,status="pending")

        if patient_created:
            messages.success(
                request,
                f"নতুন অ্যাকাউন্ট তৈরি হয়েছে। "
                f"ইউজারনেম ও পাসওয়ার্ড: {phone}"
            )
        message = (
            f"A new ডেন্টাল ক্লিনিক অ্যাপয়েন্টমেন্ট কনফার্মড ✅\n\n"
            f"নাম: {patient.name}\n"
            f"তারিখ: {appointment_date}\n"
            f"সিরিয়াল: {serial}\n"
            f"সময়: {time.strftime('%I:%M %p')}\n\n"
            f"Phone: {phone}\n"
            f"cause: {problem}"
        )
        phone = '01957536572'
        send_whatsapp(phone, message)


        messages.success(
            request,
            f"অ্যাপয়েন্টমেন্ট সফল। সিরিয়াল #{serial}, সময় {time.strftime('%I:%M %p')}"
        )
        return redirect("appointment")
    return render(request, "core/appointment.html")


# Patient login page
def patient_login(request):
    return render(request, 'core/login.html')

# Chamber page
def chamber(request):
    return render(request, 'core/chamber.html')
