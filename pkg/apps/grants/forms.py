from django import forms
from .models import Questionnaire


class QuestionnaireForm(forms.ModelForm):
    
    class Meta:
        model = Questionnaire 
        fields = (
            "location", "type_of_applicant", 
            "type_of_fund", "objectives", 
            "background"
        )