from dotenv import load_dotenv
load_dotenv()
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage , SystemMessage , ToolMessage
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langsmith import traceable

MAX_ITERATIONS  = 10
MODEL = "gpt-oss:latest"

@tool
def get_product_price(product:str) -> float:
    """check the price of a product"""
    print(f"Checking the price of {product}")
    product_Obj = {
        "phone":1000,
        "laptop":1500,
        "tablet":500,
    }
    return product_Obj.get(product,0)

@tool
def discounted_price(price:float , offer_name:str) -> float:
    """It will check the offer and apply the offer and return discounted price"""
    print(f" product price = {price} , discount offer is = {offer_name}")
    discount_offer = {
        "gold":20 ,
        "silver":15,
        "bronze" : 10
        }
    after_discount_price =  price - (price * (discount_offer.get(offer_name , 0) / 100))
    print(after_discount_price)
    return round(after_discount_price ,2)

@traceable(name = "Langchain agent loop")
def run_agent(question:str):
   # pass
   tools = [get_product_price,discounted_price]
   tools_dict = {t.name: t for t in tools}
   
   llm = init_chat_model(f"ollama:{MODEL}" , temperature=0)
   llm_with_tools = llm.bind_tools(tools)

   messages = [
    SystemMessage(
        content(
                "You are a helpful shopping assistant. "
                "You have access to a product catalog tool "
                "and a discount tool.\n\n"
                "STRICT RULES — you must follow these exactly:\n"
                "1. NEVER guess or assume any product price. "
                "You MUST call get_product_price first to get the real price.\n"
                "2. Only call apply_discount AFTER you have received "
                "a price from get_product_price. Pass the exact price "
                "returned by get_product_price — do NOT pass a made-up number.\n"
                "3. NEVER calculate discounts yourself using math. "
                "Always use the apply_discount tool.\n"
                "4. If the user does not specify a discount tier, "
                "ask them which tier to use — do NOT assume one."
        )
    ),
    HumanMessage(content=question),
   ]

run_agent("what is the price of laptop after gold discount")