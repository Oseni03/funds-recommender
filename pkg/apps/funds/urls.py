from django.urls import path

from . import views

app_name = "funds"

urlpatterns = [
    path("profile/", views.FundProfileView.as_view(), name="profile"),
    path("<slug:slug>/", views.FundView.as_view(), name="fund"),
    path("", views.FundView.as_view(), name="funds"),
]