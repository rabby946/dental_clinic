from django.urls import path
from . import views

app_name = 'medicines'

urlpatterns = [
    path('', views.medicine_list, name='list'),
    path('add/', views.medicine_create, name='create'),
]
