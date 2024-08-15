from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import os
import openai
import sys

sys.path.append("../..")

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(model="gpt-4o-mini")
uri = "sqlite:///northwind.db"
dbname = "Northwind"


def get_engine_for_northwind_db():
    return create_engine(
        "sqlite:///northwind.db",
        poolclass=StaticPool,
    )


def get_db():
    engine = get_engine_for_northwind_db()
    db = SQLDatabase(engine)
    return db


toolkit = SQLDatabaseToolkit(db=get_db(), llm=llm)
db_tools = toolkit.get_tools()
 


# prompt = hub.pull("hwchase17/openai-tools-agent")
#
#
#
# agent = create_openai_tools_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools)
#
# result = agent_executor.invoke({"input": "What is the total number of employees?"})
#
# #print(result)
