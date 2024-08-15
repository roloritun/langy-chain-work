from langchain_core.prompts import ChatPromptTemplate

def get_prompt_for_openai_functions_agent():
    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
    ])
    return prompt
    
    

def get_prompt_for_openai_tools_agent():  
    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
    ])
    return prompt

