from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()


@tool
def search(query: str) -> str:
    """Search the web for information about a query."""
    print(f"Searching for: {query}")
    return "This is a test search result"


llm = ChatOllama(temperature=0.0, model="gpt-oss:latest")
tools = [search]
agent = create_agent(model=llm, tools=tools)
result = agent.invoke(
    {"messages": [HumanMessage(content="What is the capital of France?")]}
)
print(result)