from django import forms
from .models import FundProfile


class FundProfileForm(forms.ModelForm):
    
    class Meta:
        model = FundProfile 
        fields = (
            "title", "location", "objectives", 
            "fund_type", "fund_category", "eligibility", 
            "estimated_budget", "background", "project_summary",  
        )