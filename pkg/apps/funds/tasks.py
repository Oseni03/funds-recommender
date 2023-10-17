from celery import shared_task

from .models import FundProfile, Fund
from .utils import get_summary, create_doc, store_docs

template = """
You are a professional grant writer with skills such as Attention to detail, Organizational skills, Research skills, Practical thinking and Persistence.

A grant writer is responsible for assembling and sending out a company or organization's proposals for grants.
A grant writer goal is to assist organizations with applying and qualifying for as many grants as possible. Some responsibility of a grant writer include: Researching grants, Reviewing grant guidelines, Creating proposals and Communicating with clients and donors.

Given the text below, generate a concise and short summary of the text which can be used to determine grant opportunity match for the specific user without leaving out any detail.
Remember, do not include any information not mentioned in the text.

{text}

CONCISE SUMMARY:"""


@shared_task
def get_fund_summary(fund_id, texts):
    instance = Fund.objects.get(id=fund_id)
    output = get_summary(template, texts)
    
    print(output)
    
    instance.summary = output
    instance.save()
    
    doc = create_doc(
        output, 
        fund_id=instance.id, 
        opportunity_no=opportunity_no, 
        posted_date=posted_date, 
        last_updated_date=last_updated_date, 
        closing_date=closing_date
    )
    
    store_docs("funds_index", [doc])


@shared_task
def get_profile_summary(profile_id, texts):
    instance = FundProfile.objects.get(id=profile_id)
    output = get_summary(template, texts)
    
    print(output)
    
    instance.summary = output
    instance.save()
    
    doc = create_doc(
        output, 
        profile_id=instance.id, 
        user_id=instance.user.id, 
        estimated_budget=instance.estimated_budget
    )
    
    store_docs("profiles_index", [doc])