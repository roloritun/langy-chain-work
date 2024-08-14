# FastAPI api
from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings

from resource import run_agent


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENWEATHERMAP_API_KEY: str
    PINECONE_API_KEY: str
    USER_AGENT: str

    class Config:
        env_file = ".env"


settings = Settings()
app = FastAPI()


def get_app_description():
    return (
        "\n"
        "        Welcome to the Langchain Agent Test API!\n"
        "    	This API to query the northwind db, openweather api and rest countries json repo with natural language.\n"
        "    	Use the '/ask/' endpoint with a POST request to query.\n"
        "    	Example usage: POST to '/ask/' with JSON data containing input\n"
        "    	"
    )


@app.get("/")
def root():
    return {"message": get_app_description()}


# Endpoint
@app.get("/ask", dependencies=[Depends(run_agent)])
def ask_a_question(question: str):
    return run_agent(question)
