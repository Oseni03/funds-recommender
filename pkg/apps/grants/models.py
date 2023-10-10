from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings

# Create your models here.
class Questionnaire(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, help_text=_("Your geographic scope"))
    type_of_applicant = models.CharField(max_length=255, help_text=_("eg. Individual, small business, etc"))
    type_of_fund = models.CharField(max_length=255, help_text=_("eg. Capital, general operating, etc"))
    objectives = models.TextField(help_text=_("Your mission and goals"))
    background = models.TextField(help_text=_("Little about your history"))
    # price_range = models.BigIntegerRangeField() # or IntegerRangeField