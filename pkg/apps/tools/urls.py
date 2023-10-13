from django.urls import path

from . import views

app_name = "tools"

urlpatterns = [
    path("writer/", views.WriterView.as_view(), name="writer"),
]