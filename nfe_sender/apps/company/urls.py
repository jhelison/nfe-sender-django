from django.urls import path
from apps.company import views

urlpatterns = [
    path("", views.root),
    path("sign-in/", views.sign_in, name="sign-in"),
    path("recover/", views.recover_token, name="recover"),
]
