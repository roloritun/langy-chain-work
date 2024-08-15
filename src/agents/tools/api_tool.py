from pydantic import BaseModel, Field

from langchain_community.tools import OpenWeatherMapQueryRun
from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper
from langchain_openai import ChatOpenAI
import openai
import os

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

OpenWeatherMapAPIWrapper.api_key = os.environ['OPENWEATHERMAP_API_KEY']

openai.api_key = os.environ['OPENAI_API_KEY']

llm = ChatOpenAI(model="gpt-4o-mini")


class OpenWeatherInput(BaseModel):
    location: str = Field(..., description="Latitude of the location to fetch weather data for")


open_weather = OpenWeatherMapQueryRun(api_wrapper=OpenWeatherMapAPIWrapper())


api_tools = [open_weather]

# prompt = hub.pull("hwchase17/openai-functions-agent")
#
# agent = create_openai_functions_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools)
#
# result = agent_executor.invoke({"input": "What is the current weather Nigeria"})
# print(result)
