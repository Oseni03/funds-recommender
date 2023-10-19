from django.db.models.signals import post_save
from django.dispatch import Signal
from django.dispatch import receiver

from .models import FundProfile, Fund
from .tasks import get_fund_summary, get_profile_summary


@receiver(post_save, sender=FundProfile)
def create_profile_summary(sender, instance, created, **kwargs):
    texts = instance.objectives + "\n" + instance.project_summary + "\n" + instance.background
    
    get_profile_summary.delay(instance.id, texts)


@receiver(post_save, sender=Fund)
def create_fund_summary(sender, instance, created, **kwargs):
    if created:
        texts = instance.eligibility_info + "\n" + instance.description
        
        get_fund_summary.delay(instance.id, texts)