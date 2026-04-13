# apps/accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', views.password_change_view, name='password_change'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # User Management
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]