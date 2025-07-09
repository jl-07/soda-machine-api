from openai import OpenAI
from instructor import from_openai
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = from_openai(openai_client)

class ParsedCommand(BaseModel):
    intent: str
    soda_type: str
    quantity: int

def parse_message(message: str) -> ParsedCommand:
    messages = [{"role": "user", "content": message}]
    result = client.create(ParsedCommand, messages=messages, model="gpt-3.5-turbo")
    if isinstance(result.quantity, str):
        result.quantity = int(result.quantity)
    return result