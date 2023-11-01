from langchain import OpenAI, LLMChain
from langchain.memory import ConversationBufferWindowMemory

from .prompts import generate_writer_prompt


def get_writer_chain(add_summary):
    prompt = generate_writer_prompt(add_summary)
    
    writer_chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=prompt,
        verbose=False,
    )
    return writer_chain