from langchain_openai import OpenAI, ChatOpenAI
from langchain import hub
import os
import openai
from api_sources import api_tools
from db_helper_tool import db_tools
from web import web_tools
from langchain.agents import create_openai_functions_agent, AgentExecutor, create_openai_tools_agent
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.environ['OPENAI_API_KEY']


def run_agent(question: str):
    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt = hub.pull("hwchase17/openai-functions-agent")

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
