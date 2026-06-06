from unittest.mock import MagicMock, patch
from langchain.messages import AIMessage, HumanMessage
from langgraph.types import Command

from language_tutor.agent.nodes import call_japanese_tutor, call_grammar_critic
from language_tutor.agent.schemas import GrammarCriticSchema
from language_tutor.agent.state import AgentState


# ================ Japanese Tutor Tests ================


@patch("language_tutor.agent.nodes.get_llm")
@patch("language_tutor.agent.nodes.get_node_config")
def test_japanese_tutor_node(mock_config, mock_get_llm):
    """
    Tests the japanese_tutor node runs and returns the expected output.
    """

    # Variables
    user_message = "こんにちは。"
    bot_response = "こんにちは！今日はお元気ですか？"

    # Set the return values for patch overrides
    mock_config.return_value = ("mock-model-name", "mock system prompt", 0.0)

    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(content=bot_response)
    mock_get_llm.return_value = mock_llm

    # Create initial state
    mock_state = AgentState(
        user_input=user_message,
        chat_history=[],
        bot_response="",
        feedback_notes="",
        corrected_input="",
    )

    # Invoke node
    result = call_japanese_tutor(mock_state)

    # Check output
    assert isinstance(result, dict)
    assert len(result) == 2
    assert result["bot_response"] == bot_response
    assert len(result["chat_history"]) == 2
    assert isinstance(result["chat_history"][0], HumanMessage)
    assert result["chat_history"][0].content == user_message
    assert isinstance(result["chat_history"][1], AIMessage)
    assert result["chat_history"][1].content == bot_response


# ================ Grammar Critic Tests ================


@patch("language_tutor.agent.nodes.get_structured_llm")
@patch("language_tutor.agent.nodes.get_node_config")
def test_grammar_critic_path_true(mock_config, mock_get_llm):
    """
    Tests the grammar_critic node when the user's message has correct grammar.
    Checks the node correct type as expected.
    """

    # Set return values for patch overrides
    mock_config.return_value = ("mock-model-name", "mock system prompt", 0.0)

    mock_llm = MagicMock()
    mock_llm.invoke.return_value = GrammarCriticSchema(
        is_correct=True, correction="", explanation=""
    )
    mock_get_llm.return_value = mock_llm

    # Create initial state
    mock_state = AgentState(
        user_input="私は海に泳ぎます。",
        chat_history=[],
        bot_response="",
        feedback_notes="",
        corrected_input="",
    )

    # Invoke node
    result = call_grammar_critic(mock_state)

    # Check output
    assert isinstance(result, Command)
    assert result.goto == "japanese_tutor"
    assert result.update["feedback_notes"] == ""


@patch("language_tutor.agent.nodes.get_structured_llm")
@patch("language_tutor.agent.nodes.get_node_config")
def test_grammar_critic_path_false(mock_config, mock_get_llm):
    """
    Tests the grammar_critic node when the user's message has wrong grammar.
    Checks the node returns the correct type as expected.
    """

    # Set return values for patch overrides
    mock_config.return_value = ("mock-model-name", "mock system prompt", 0.0)

    mock_llm = MagicMock()
    mock_llm.invoke.return_value = GrammarCriticSchema(
        is_correct=False,
        correction="私は海で泳ぎます。",
        explanation="Used に instead of で...",
    )
    mock_get_llm.return_value = mock_llm

    # Create initial state
    mock_state = AgentState(
        user_input="私は海に泳ぎます。",
        chat_history=[],
        bot_response="",
        feedback_notes="",
        corrected_input="",
    )

    # Invoke node
    result = call_grammar_critic(mock_state)

    # Check output
    assert isinstance(result, Command)
    assert result.goto == "japanese_tutor"
    assert result.update["feedback_notes"] == "Used に instead of で..."
    assert result.update["corrected_input"] == "私は海で泳ぎます。"
