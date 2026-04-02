# apps/schools/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django_tenants.utils import schema_context

from .forms import SchoolSignupForm
from .models import School, Domain
from accounts.models import User

def index(request):
    return render(request, 'schools/index.html')

def school_signup(request):
    if request.method == 'POST':
        form = SchoolSignupForm(request.POST)
        if form.is_valid():
            school_name = form.cleaned_data['school_name']
            slug = form.cleaned_data['slug']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check if slug already exists
            if School.objects.filter(schema_name=slug).exists():
                messages.error(request, "This school slug is already taken.")
                return render(request, 'schools/signup.html', {'form': form})

            try:
                # 1. Create the Tenant (School)
                tenant = School(
                    name=school_name,
                    slug=slug,
                    contact_email=email,
                    trial_ends_at=timezone.now() + timedelta(days=2),
                    is_active=True,
                )
                tenant.save()   # This creates the new schema

                # 2. Create Domain (subdomain)
                Domain.objects.create(
                    domain=f"{slug}.localhost",   # Change to your real domain in production
                    tenant=tenant,
                    is_primary=True
                )

                # 3. Create First Admin User INSIDE the new tenant schema
                with schema_context(tenant.schema_name):
                    admin_user = User.objects.create_user(
                        username="admin",
                        email=email,
                        password=password,
                        role=User.Role.ADMIN,
                        is_staff=True,
                        is_superuser=True,
                    )
                    admin_user.force_password_change = False
                    admin_user.save()

                messages.success(request, f"School '{school_name}' created successfully!")
                # Redirect to the new school's login page
                return redirect(f"http://{slug}.localhost:8000/login/")  # Change to your real domain in production 

            except Exception as e:
                print(f"Error creating school: {str(e)}")
                return render(request, 'schools/signup.html', {'form': form})

    else:
        form = SchoolSignupForm()

    return render(request, 'schools/signup.html', {'form': form})