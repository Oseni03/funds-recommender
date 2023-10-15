from celery import shared_task
from django.conf import settings

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from .models import FundProfile, Fund

template = """
You are a professional grant writer with years of experience. 
Given the text below, generate a concise summary of the text which can be used to determine grant opportunity match for the specific user without leaving out any detail.

{text}

CONCISE SUMMARY:"""


def get_summary(template, texts):
    prompt = PromptTemplate.from_template(template)
    
    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", openai_api_key=settings.OPENAI_API_KEY)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, 
        document_variable_name="text"
    )
    return stuff_chain.run(texts)


@shared_task
def get_fund_summary(fund_id, texts):
    instance = Fund.objects.get(id=fund_id)
    output = get_summary(template, texts)
    
    print(output)
    
    instance.summary = output
    instance.save()


@shared_task
def get_profile_summary(profile_id, texts):
    instance = FundProfile.objects.get(id=profile_id)
    output = get_summary(template, texts)
    
    print(output)
    
    instance.summary = output
    instance.save()