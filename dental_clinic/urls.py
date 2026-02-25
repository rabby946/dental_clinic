
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('apps.core.urls')),

    path(
        'patients/',
        include(('apps.patients.urls', 'patients'), namespace='patients')
    ),

    path(
        'doctors/',
        include(('apps.doctors.urls', 'doctors'), namespace='doctors')
    ),

    path(
        'medicines/',
        include(('apps.medicines.urls', 'medicines'), namespace='medicines')
    ),

    path(
        'billing/',
        include(('apps.billing.urls', 'billing'), namespace='billing')
    ),

    path(
        'prescriptions/',
        include(('apps.prescriptions.urls', 'prescriptions'), namespace='prescriptions')
    ),
]


