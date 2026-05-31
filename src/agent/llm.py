import os
from typing import Type
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def get_llm(model_name: str, temperature: float):
    """
    Returns a LangChain Google chat model interface.

    Takes a model name and temperature.
    Will automatically insert the API key from the .env file.

    Args:
        model_name: The name of the llm e.g. 'gemini-3.1-flash-lite'
        temperature: Temperature of the llm..

    Returns:
        A LangChain model interface.

    Raises:
        ValueError: If 'GOOGLE_API_KEY' not found in environment variables.
    """
    # Check API key exists
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("'GOOGLE_API_KEY' is missing from environment variables. Add it to a .env file.")

    return ChatGoogleGenerativeAI(
        model=model_name,
        api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=temperature,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

def get_structured_llm(model_name: str, schema: Type[BaseModel], temperature: float):
    """
    Returns a structured LangChain Google chat model interface.

    Takes a model name and temperature,
    returns a model inteface that has a set structed output based on your schema.
    Will automatically insert the API key from the .env file.

    Args:
        model_name: The name of the llm e.g. 'gemini-3.1-flash-lite'
        schema: A Pydantic BaseModel of the return format you require. 
        temperature: Temperature of the llm. Defaults to 1.0 (The same as LangChain).

    Returns:
        A LangChain model interface with structured output.

    Raises:
        ValueError: If 'GOOGLE_API_KEY' not found in environment variables.
    """
    # Get base model
    llm = get_llm(model_name=model_name, temperature=temperature)

    # Bind the schema to the model
    return llm.with_structured_output(schema=schema)