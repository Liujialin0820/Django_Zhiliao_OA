from django.urls import path
from apps.myuser.views import LoginView

app_name = "myuser"

urlpatterns = [
    path("login/", LoginView.as_view()),
]
