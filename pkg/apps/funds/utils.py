from django.conf import settings

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI

import pinecone


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


def store_fund_summary_embeddings(index_name, docs):
    # initialize pinecone
    pinecone.init(
        api_key=settings.PINECONE_API_KEY,  # find at app.pinecone.io
        environment=settings.PINECONE_ENV,  # next to api key in console
    )
    
    # First, check if our index already exists. If it doesn't, we create it
    if index_name not in pinecone.list_indexes():
        # we create a new index
        pinecone.create_index(
          name=index_name,
          metric='cosine',
          dimension=1536  
    )
    # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    
    docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    return docsearch


def get_fund_relevant_docs(index_name, profile_summary_vector):
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    
    docs = docsearch.similarity_search_by_vector_with_score(profile_summary_vector, k=5)
    # returns → List of Tuples of (doc, similarity_score)
    return docs 