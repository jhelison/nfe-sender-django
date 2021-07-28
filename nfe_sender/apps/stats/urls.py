from django.urls import path
from apps.stats import views

urlpatterns = [
    path("status/", views.server_status, name="stats-status"),
    path("", views.stats_root),
]
