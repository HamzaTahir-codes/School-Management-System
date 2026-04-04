from django.urls import path
from . import views

app_name = 'grading'

urlpatterns = [
    path('marks/', views.MarkListView.as_view(), name='mark_list'),
    path('marks/add/', views.MarkCreateView.as_view(), name='mark_add'),
    path('marks/<int:pk>/edit/', views.MarkUpdateView.as_view(), name='mark_edit'),
    path('marks/<int:pk>/delete/', views.MarkDeleteView.as_view(), name='mark_delete'),

    path('reports/', views.FinalReportListView.as_view(), name='report_list'),
    path('reports/add/', views.FinalReportCreateView.as_view(), name='report_add'),
    path('reports/<int:pk>/edit/', views.FinalReportUpdateView.as_view(), name='report_edit'),
    path('reports/<int:pk>/delete/', views.FinalReportDeleteView.as_view(), name='report_delete'),
]