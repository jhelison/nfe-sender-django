from django.urls import path
from apps.services import views

urlpatterns = [
    path("", views.root),
    path("nfestatusservico/", views.nfe_status_servico, name="services-status"),
]
