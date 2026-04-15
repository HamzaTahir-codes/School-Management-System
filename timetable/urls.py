from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    # Presets
    path('presets/', views.TimingPresetListView.as_view(), name='preset_list'),
    path('presets/add/', views.TimingPresetCreateView.as_view(), name='preset_add'),
    path('presets/<int:pk>/edit/', views.TimingPresetUpdateView.as_view(), name='preset_edit'),
    
    # Slots
    path('presets/<int:preset_pk>/slots/', views.TimeSlotListView.as_view(), name='slot_list'),
    path('presets/<int:preset_pk>/slots/add/', views.TimeSlotCreateView.as_view(), name='slot_add'),
    
    # Grid Builder
    path('builder/', views.TimetableBuilderView.as_view(), name='builder'),
    path('builder/assign/', views.assign_period, name='assign_period'),
    path('builder/remove/<int:entry_pk>/', views.remove_period, name='remove_period'),

    # Substitution
    path('substitutions/', views.SubstitutionListView.as_view(), name='sub_list'),
    path('substitutions/add/', views.SubstitutionCreateView.as_view(), name='sub_add'),

    # Day Override
    path('overrides/', views.WorkdayOverrideListView.as_view(), name='override_list'),
    path('overrides/add/', views.WorkdayOverrideCreateView.as_view(), name='override_add'),

    # Extensions
    path('extensions/', views.ExtensionApprovalListView.as_view(), name='extension_list'),
    path('extensions/<int:pk>/approve/', views.approve_extension, name='approve_extension'),

    # Teacher Views
    path('schedule/', views.TeacherScheduleView.as_view(), name='teacher_schedule'),
    path('request-extension/', views.request_attendance_extension, name='request_extension'),
]
