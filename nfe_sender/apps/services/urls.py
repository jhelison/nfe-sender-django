from django.urls import path
from apps.services import views

urlpatterns = [
    path("", views.root),
    path("StatusServico/", views.StatusServico.as_view(), name="services-status"),
    path(
        "ConsultaProtocolo/",
        views.ConsultaProtocolo.as_view(),
        name="consulta-protocolo",
    ),
]
