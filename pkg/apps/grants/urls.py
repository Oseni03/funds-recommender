from django.urls import path

from . import views

app_name = "grants"

urlpatterns = [
    path("questionnaire/", views.QuestionnaireView.as_view(), name="questionnaire"),
]