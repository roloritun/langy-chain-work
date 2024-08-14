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
# class UserRefPromptInput(BaseModel):
#     """get_info_from_prompt"""
#     question: str = Field(description="question from the prompt")


# class NW_Tool(BaseTool):
#     name = dbname
#     description = """
#         This is the @northwind database tool. Use it when questions make reference to the database. \
#         It is useful when user want to read data or answer questions regarding information stored in the \
#         northwind database
#         """
#     args_schema: Type[BaseModel] = UserRefPromptInput
#
#     def _run(self, question: str):
#         agent = create_sql_agent(
#             llm,
#             db=get_db(),
#             prompt=prompt,
#             agent_type="openai-tools",
#             verbose=True,
#         )
#         response = agent.invoke({"input": question})
#         print(response)
#         return response
#
#     def _arun(self, question: str):
#         raise NotImplementedError("does not support async")


# tools = [NW_Tool()]


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
