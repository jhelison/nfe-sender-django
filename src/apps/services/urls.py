from django.urls import path
from apps.services import views

urlpatterns = [
    path("", views.root_view),
    path("status-servico/", views.StatusServicoView.as_view(), name="services-status"),
    path(
        "consulta-protocolo/",
        views.ConsultaProtocoloView.as_view(),
        name="consulta-protocolo",
    ),
]
