from django.urls import path
from apps.services import views

urlpatterns = [
    path("", views.root_view),
    path("StatusServico/", views.StatusServicoView.as_view(), name="services-status"),
    path(
        "ConsultaProtocolo/",
        views.ConsultaProtocoloView.as_view(),
        name="consulta-protocolo",
    ),
]
