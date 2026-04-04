# School Management System - Implementation Plan

This is a comprehensive plan to build out the features of the multi-tenant School Management System. Now that tenant signup is complete, we will focus on implementing the per-tenant features: Authentication, Role-based Dashboards, User Profiles, and the core operational apps.

## User Review Required

> [!IMPORTANT]
> **Design Strategy & Aesthetics**: The plan includes a focus on high-quality visual aesthetics, emphasizing a modern, responsive, and intuitive UI using custom CSS or a lightweight framework without relying entirely on un-styled native forms. Do you have a preferred CSS framework for this project (e.g., TailwindCSS, Bootstrap), or should we use custom Vanilla CSS for a tailored premium look?

> [!TIP]
> **Dashboard Routing Strategy**: After login, users (Admin, Teacher, Parent, Student) will be routed to a single `dashboard_view` which dynamically renders different content/widgets based on their `role`. Does this align with your vision, or do you prefer entirely separate dashboard URLs for each role?

## Proposed Changes

---

### authentication & accounts (`accounts` app)
Implementing secure login, logout, password management, and role-based redirect dashboards.

#### [MODIFY] `accounts/views.py`
- Replace stubs with actual Django Views. Use `LoginView` and `LogoutView` from `django.contrib.auth`.
- Implement `dashboard_view` that retrieves the logged-in user's role and renders the appropriate dashboard template.

#### [NEW] `accounts/forms.py`
- Create a customized `AuthenticationForm` to add specific CSS classes or validations.

#### [NEW] `templates/base.html`
- A master template containing the global navigation sidebar, header, and styling tokens.

#### [NEW] `templates/accounts/login.html`
- A premium, aesthetically pleasing login page showcasing the tenant system (school name displayed dynamically).

#### [NEW] `templates/accounts/dashboards/`
- `admin_dashboard.html`, `teacher_dashboard.html`, `student_dashboard.html`, `parent_dashboard.html` for role-specific interfaces.

---

### user profiles & management (`people` app)
Enabling admins to add Teachers, Students, and Parents. Handing the automatic creation of their `User` accounts.

#### [MODIFY] `people/views.py`
- Implement Class-Based Views (CBVs) for List, Create, Update, and Delete operations for `StudentProfile`, `TeacherProfile`, and `ParentProfile`.

#### [NEW] `people/forms.py`
- Create complex forms that simultaneously handle creating a base `User` (with a generated password) and the associated `Profile` in one step.

#### [NEW] `templates/people/`
- Professional data tables and forms for managing school personnel and students.
- Profile viewer pages showing relevant info (e.g., a Student's Profile will show their current class, parent details, and status).

#### [MODIFY] `people/urls.py`
- Map the CRUD routes for teachers, parents, and students.

---

### academics foundation (`academics` app)
Managing Classes, Sections, and Timetables.

#### [MODIFY] `academics/models.py`
- Define `ClassLevel`, `Section`, `Subject` if not already fully fleshed out.

#### [MODIFY] `academics/views.py` & `academics/urls.py`
- Views for School Admins to set up the academic structure (Adding Classes, adding Sections, assigning Subjects to Classes).

---

### Phase 4+ Iterations (Post-Foundation)
Once the above core features are built, we will sequentially tackle:
1. **Attendance**: Daily attendance logging interface for Teachers.
2. **Grading**: Exam creation, marks entry, and report card generation.
3. **Fees**: Automatic invoice generation, parent payment tracking.

## Open Questions

> [!WARNING]
> **Authentication Method**: Are we going to support Email-based login, Username-based login, or both? (The default Django `AbstractUser` favors username, but often Schools prefer email or Admission/Roll Number for students).

## Verification Plan

### Automated Tests
- Test that unauthorized users cannot access the dashboard or profile pages.
- Test that each role (Admin, Teacher, Staff) sees only their respective dashboard layout after a successful login.

### Manual Verification
- Start the server and create a sample tenant.
- Visit the tenant's exact URL (e.g., `http://test-school.localhost:8000/login/`).
- Log in and verify that the UI looks modern, premium, and functional.
- Attempt to create a Teacher Profile and ensure the associated base `User` account is created successfully.
