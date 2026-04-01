from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login_view(request):
    return HttpResponse("Login Page - Implement your login form here")

def logout_view(request):
    return HttpResponse("Logout Page - Implement your logout logic here")

def password_change_view(request):
    return HttpResponse("Password Change Page - Implement your password change form here")

def dashboard_view(request):
    return HttpResponse("Dashboard Page - Implement your dashboard logic here")