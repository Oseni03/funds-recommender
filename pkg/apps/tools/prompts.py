from langchain import PromptTemplate

def generate_writer_prompt(add_summary):
    if add_summary:
        template = """Act as an expert grant writer and a business owner. 
        The grant application is asking you: "{question}" You are going to respond in a .{formatted_tone} tone of voice. You have a {writing_style} writing style. 
        To give more background, {summary}
        
        Answer:"""
        prompt = PromptTemplate(input_variables=["question", "formatted_tone", "writing_style", "summary"], template=template)
    else:
        template = """Act as an expert grant writer and a business owner. 
        The grant application is asking you: "{question}" You are going to respond in a .{formatted_tone} tone of voice. You have a {writing_style} writing style. 
        
        Answer:"""
        prompt = PromptTemplate(input_variables=["question", "formatted_tone", "writing_style"], template=template)
    return prompt
