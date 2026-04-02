from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    # Academic Session
    path('sessions/', views.SessionListView.as_view(), name='session_list'),
    path('sessions/add/', views.SessionCreateView.as_view(), name='session_add'),
    
    # Class Levels
    path('classes/', views.ClassListView.as_view(), name='class_list'),
    path('classes/add/', views.ClassCreateView.as_view(), name='class_add'),
    
    # Sections
    path('sections/', views.SectionListView.as_view(), name='section_list'),
    path('sections/add/', views.SectionCreateView.as_view(), name='section_add'),
    
    # Subjects
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject_add'),
]
