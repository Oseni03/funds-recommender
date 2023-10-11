from django.shortcuts import render
from django.views.generic import FormView

from .forms import FundProfileForm

# Create your views here.
class FundProfileView(FormView):
    form_class = FundProfileForm
    template_name = "funds/profile.html"