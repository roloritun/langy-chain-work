from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import time


from langchain_openai import ChatOpenAI
import openai
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.environ["OPENAI_API_KEY"]
llm = ChatOpenAI(temperature=0)

country_url = "https://restcountries.com/v3.1/all"


def get_countries_json():
    loader = WebBaseLoader(
        web_paths=(country_url,),
    )
    countries_json = loader.load()
    return countries_json


def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    splits = text_splitter.split_documents(documents)
    return splits


def store_vector_retriever(splits, index_name="langchain-json"):
    # initialize pine cone

    pc = Pinecone()

    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if index_name not in existing_indexes:
        # pc.delete_index(index_name)
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    index = pc.Index(index_name)
    vector_store = PineconeVectorStore(index=index, embedding=OpenAIEmbeddings())
    # vector_store.add_documents(splits)
    return vector_store


def get_country_tool():
    docs = get_countries_json()
    splits = split_docs(docs)
    vector_store = store_vector_retriever(splits)
    retriever = vector_store.as_retriever()
    tool = create_retriever_tool(
        retriever=retriever,
        name="country_json_retriever",
        description="Searches and returns country details",
    )
    return tool


web_tools = [get_country_tool()]

# prompt = hub.pull("hwchase17/openai-tools-agent")
#
#
#
# agent = create_openai_tools_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools)
#
# result = agent_executor.invoke({"input": "Tell me about Nigeria"})
#
# #print(result)
