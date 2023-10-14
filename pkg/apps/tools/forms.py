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


class WritingToolForm(forms.Form):
    profile = forms.ModelChoiceField(queryset=None, widget=ProfileSelect)
    query = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(dir(self))
        self.fields["profile"].queryset = models.FundProfile.objects.filter(user=self.user)