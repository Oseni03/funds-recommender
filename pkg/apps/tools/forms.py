from django import forms 

from apps.funds import models


class ProfileSelect(forms.Select):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value:
            option["attrs"]["data-summary"] = value.instance.summary
        return option


TONE_CHOICES = [
    ("sarcastic", "Sarcastic"),
    ("enthusiastic", "Enthusiastic"),
    ("motivated", "Motivated"),
    ("friendly", "Friendly"),
    ("energetic", "Energetic"),
    ("informative", "Informative"),
]

STYLE_CHOICES = [
    ("narrative", "Narrative"),
    ("descriptive", "Descriptive"),
]

class WritingToolForm(forms.Form):
    profile = forms.ModelChoiceField(queryset=None, widget=ProfileSelect)
    question = forms.CharField()
    tones = forms.MultipleChoiceField(choices=TONE_CHOICES, label="Tone")
    style = forms.ChoiceField(choices=STYLE_CHOICES, label="Writing style")
    add_profile_summary = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(dir(self))
        self.fields["profile"].queryset = models.FundProfile.objects.filter(user=self.user)
    
    def formatted_tones(self):
        tones = self.cleaned_data.get("tone")
        formatted
        while tones:
            if len(tones) > 2:
                formatted += f"{tones.pop()}, "
            elif len(tones) == 2:
                formatted += f"{tones.pop()} and "
            else:
                formatted += f"{tones.pop()}"
        return formatted