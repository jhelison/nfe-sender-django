from django.urls import path
from apps.NFe import views

urlpatterns = [
    path("", views.root_view),
    path("autorizacao/", views.AutorizacaoView.as_view(), name="autorizacao"),
    path("cancelamento/", views.CancelamentoView.as_view(), name="cancelamento"),
]
