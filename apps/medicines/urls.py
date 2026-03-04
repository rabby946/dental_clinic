from django.urls import path
from . import views

app_name = 'medicines'

urlpatterns = [
    path('', views.medicine_manage, name='manage'),
]
