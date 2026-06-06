import os
from unittest.mock import patch
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable

from language_tutor.agent.llm import get_llm, get_structured_llm
from language_tutor.agent.schemas import GrammarCriticSchema


@patch.dict(os.environ, {"GOOGLE_API_KEY": "mock_api_key"})
def test_get_llm():
    """
    Tests that the get_llm function correctly returns the expected type
    """

    result = get_llm(model_name="mock-model-name", temperature=0.3)

    assert isinstance(result, BaseChatModel)

    assert result.model == "mock-model-name"
    assert result.temperature == 0.3


@patch.dict(os.environ, {"GOOGLE_API_KEY": "mock_api_key"})
def test_get_structured_llm():
    """
    Tests that the get_structured_llm function correctly returns the expected type
    """

    result = get_structured_llm(
        model_name="mock-model-name", schema=GrammarCriticSchema, temperature=0.0
    )

    assert isinstance(result, Runnable)
