from django.urls import path
from apps.NFe import views

urlpatterns = [
    path("", views.root_view),
    path("autorizacao/", views.AutorizacaoView.as_view(), name="autorizacao"),
    path("cancelamento/", views.CancelamentoView.as_view(), name="cancelamento"),
    path("carta-correcao/", views.CartaView.as_view(), name="carta-correcao"),
]
