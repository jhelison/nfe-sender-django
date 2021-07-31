from django.urls import path
from apps.services import views

urlpatterns = [
    path("", views.root),
    path("nfestatusservico/", views.NfeStatusServico.as_view(), name="services-status"),
]
