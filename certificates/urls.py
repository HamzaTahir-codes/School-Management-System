from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('directory/', views.CertificateListView.as_view(), name='certificate_list'),
    path('generate/', views.CertificateCreateView.as_view(), name='certificate_add'),
    path('<int:pk>/edit/', views.CertificateUpdateView.as_view(), name='certificate_edit'),
    path('<int:pk>/delete/', views.CertificateDeleteView.as_view(), name='certificate_delete'),
]