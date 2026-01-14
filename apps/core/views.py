from django.shortcuts import render, redirect
from django.contrib import messages
# Home page
def home(request):
    return render(request, 'core/home.html')

# Services page
def services(request):
    return render(request, 'core/services.html')

# Contact page
def contact(request):
    return render(request, 'core/contact.html')

# Appointment page
def appointment(request):
    if request.method == "POST":
        # handle form
        messages.success(request, "আপনার অ্যাপয়েন্টমেন্ট সফলভাবে বুক হয়েছে!")
        return redirect('appointment')
    return render(request, 'core/appointment.html')

# Patient login page
def patient_login(request):
    return render(request, 'core/login.html')

# Chamber page
def chamber(request):
    return render(request, 'core/chamber.html')
