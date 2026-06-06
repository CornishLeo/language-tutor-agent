from unittest.mock import MagicMock, patch

from langchain.messages import AIMessage

from language_tutor.agent.graph import graph
from language_tutor.agent.schemas import GrammarCriticSchema


@patch("language_tutor.agent.nodes.get_llm")
@patch("language_tutor.agent.nodes.get_structured_llm")
@patch("language_tutor.agent.nodes.get_node_config")
def test_full_graph_incorrect_grammar(
    mock_config, mock_get_structured_llm, mock_get_llm
):
    """
    Tests a full run of the graph without using any API calls.
    Uses a case that the user was wrong and the model needs to get a correction/feedback.
    """

    # Set patch overrides
    mock_config.return_value = ("mock-model-name", "mock system prompt", 0.0)

    # Mock grammar critic
    mock_critic_llm = MagicMock()
    mock_critic_llm.invoke.return_value = GrammarCriticSchema(
        is_correct=False,
        correction="私は海で泳ぎます。",
        explanation="Used に instead of で.",
    )
    mock_get_structured_llm.return_value = mock_critic_llm

    # Mock Japanese Tutor
    mock_tutor_llm = MagicMock()
    mock_tutor_llm.invoke.return_value = AIMessage(
        content="素晴らしいですね！海は綺麗でしたか？"
    )
    mock_get_llm.return_value = mock_tutor_llm

    initial_input = {"user_input": "私は海に泳ぎます。", "chat_history": []}

    # Stream the graph to get each step it completes
    steps = list(graph.stream(initial_input, stream_mode="updates"))

    assert len(steps) == 2  # grammar_critic + japanese_tutor

    # Check grammar_critic executed and updated fields
    assert "grammar_critic" in steps[0]
    critic_output = steps[0]["grammar_critic"]
    assert critic_output["feedback_notes"] == "Used に instead of で."
    assert critic_output["corrected_input"] == "私は海で泳ぎます。"

    # Check the graph dynamically routed to the tutor based on the critic's Command
    assert "japanese_tutor" in steps[1]
    tutor_output = steps[1]["japanese_tutor"]
    assert tutor_output["bot_response"] == "素晴らしいですね！海は綺麗でしたか？"

    assert "chat_history" in tutor_output
