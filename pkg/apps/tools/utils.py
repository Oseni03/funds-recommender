from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory


template = """You are a professional grant writer.

Duties and responsibilities of a grant writer here

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