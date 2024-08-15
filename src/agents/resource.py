import os

import openai
from dotenv import find_dotenv, load_dotenv
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI

from .tools.api_tool import api_tools
from .tools.db_helper_tool import db_tools
from .tools.web_tool import web_tools
from .utils.prompt import get_prompt_for_openai_functions_agent

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.environ['OPENAI_API_KEY']


def run_agent(question: str):
    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt = get_prompt_for_openai_functions_agent()

    db = db_tools
    opw = api_tools
    capi = web_tools

    tools = []
    tools.extend(db)
    tools.extend(capi)
    tools.extend(opw)

    agent = create_openai_functions_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        # verbose=True,
        # handle_parsing_errors=True,
    )
    
    result = agent_executor.invoke({"input": question})
    return result

#print(run_agent("tell about the US"))
