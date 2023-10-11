from django.urls import path

from . import views

app_name = "grants"

urlpatterns = [
    path("profile/", views.FundProfileView.as_view(), name="profile"),
]