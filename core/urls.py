from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('settings/', views.school_settings, name='school_settings'),
]