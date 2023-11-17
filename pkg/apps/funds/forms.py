from django import forms
from .models import FundProfile


class FundProfileForm(forms.ModelForm):
    class Meta:
        model = FundProfile
        fields = (
            "title",
            "location",
            "objectives",
            "applicant_type",
            "opportunity_category",
            "eligibility",
            "estimated_budget",
            "background",
            "project_summary",
        )
