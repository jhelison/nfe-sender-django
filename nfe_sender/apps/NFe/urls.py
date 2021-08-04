from django.urls import path
from apps.NFe import views

urlpatterns = [
    path("", views.root_view),
    path("autorizacao/", views.AutorizacaoView.as_view(), name="autorizacao")
]
