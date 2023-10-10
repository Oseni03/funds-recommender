from django.shortcuts import render
from django.views.generic import FormView

from .forms import QuestionnaireForm

# Create your views here.
class QuestionnaireView(FormView):
    form_class = QuestionnaireForm
    template_name = "grants/questionnaire.html"