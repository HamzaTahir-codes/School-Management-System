from django.contrib import messages
from django.shortcuts import render, redirect

def index(request):
    if not request.user.is_authenticated or request.user.role != 'ADMIN':
        messages.error(request, "You are not authorized to visit the AI Assistant page.")
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return redirect('school_index')
    return render(request, 'ai_assistant/index.html')
