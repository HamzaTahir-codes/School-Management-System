from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('structures/', views.FeeStructureListView.as_view(), name='fee_structure_list'),
    path('structures/add/', views.FeeStructureCreateView.as_view(), name='fee_structure_add'),
    path('structures/<int:pk>/edit/', views.FeeStructureUpdateView.as_view(), name='fee_structure_edit'),
    path('structures/<int:pk>/delete/', views.FeeStructureDeleteView.as_view(), name='fee_structure_delete'),

    path('payments/', views.StudentFeePaymentListView.as_view(), name='payment_list'),
    path('payments/add/', views.StudentFeePaymentCreateView.as_view(), name='payment_add'),
    path('payments/<int:pk>/edit/', views.StudentFeePaymentUpdateView.as_view(), name='payment_edit'),
    path('payments/<int:pk>/delete/', views.StudentFeePaymentDeleteView.as_view(), name='payment_delete'),
]