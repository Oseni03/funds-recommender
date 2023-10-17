from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory


template = """You are a professional grant writer with skills such as Attention to detail, Organizational skills, Research skills, Practical thinking and Persistence.

A grant writer is responsible for assembling and sending out a company or organization's proposals for grants.
A grant writer goal is to assist organizations with applying and qualifying for as many grants as possible. Some responsibility of a grant writer include: Researching grants, Reviewing grant guidelines, Creating proposals and Communicating with clients and donors.

Given a grant application question and user profile summary, generate an answer to the question

{history}

Profile summary: {summary}
Question: {question}
Answer:"""


def get_writer_chain():
    prompt = PromptTemplate(input_variables=["history", "summary", "question"], template=template)
    
    writer_chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2),
    )
    return writer_chain