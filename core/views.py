from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import SchoolIdentityForm

def school_index(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    tenant = getattr(request, 'tenant', None)
    return render(request, 'core/school_landing.html', {'school': tenant})

def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def school_settings(request):
    tenant = request.tenant
    if request.method == 'POST':
        form = SchoolIdentityForm(request.POST, request.FILES, instance=tenant)
        if form.is_valid():
            form.save()
            messages.success(request, 'School identity updated successfully!')
            return redirect('core:school_settings')
    else:
        form = SchoolIdentityForm(instance=tenant)
        
    return render(request, 'core/school_settings.html', {'form': form, 'title': 'School Identity Settings'})
